# SPDX-License-Identifier: GPL-2.0-or-later
"""GUI by default; --headless provides the identical calculation/export engine."""
import argparse
import gc
import datetime
import json
import multiprocessing
import os
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from benchmark_engine import ROOT,METHODS,make_primes,run_benchmark
from charts import figure_for,save_charts,PLOT_LOCK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk


def defaults():
    return {'repetitions':11,'target_ms':25,'timeout':120,
            'executable':str(ROOT/'bin'/('harvey_adapter.exe' if os.name=='nt' else 'harvey_adapter')),
            'harvey_max_prime':10**12,'schoof_max_prime':10**12,'bsgs_max_prime':10**13}


def fresh_output():return str(ROOT/'results'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))


class App:
    def __init__(self,root):
        self.root=root;root.title('Cartier–Miller benchmark laboratory');root.geometry('1210x850');root.minsize(950,700)
        self.events=queue.Queue();self.cancel=threading.Event();self.running=False;self.rows=[];self.canvases={}
        self.mode=tk.StringVar(value='paper');self.count=tk.StringVar(value='7');self.start=tk.StringVar(value='97');self.factor=tk.StringVar(value='10')
        self.custom=tk.StringVar();self.reps=tk.StringVar(value='11');self.timeout=tk.StringVar(value='120');self.target=tk.StringVar(value='25')
        self.output=tk.StringVar(value=fresh_output());self.executable=tk.StringVar(value=defaults()['executable']);self.queries=tk.StringVar(value='1')
        self.maxima={b:tk.StringVar(value=str(defaults()[b+'_max_prime'])) for b in ('schoof','bsgs','harvey')}
        self.selected={b:tk.BooleanVar(value=b in ('cornacchia','harvey')) for b in METHODS}
        top=ttk.Frame(root,padding=12);top.pack(fill='x')
        ttk.Label(top,text='Cartier–Miller benchmark laboratory',font=('Segoe UI',18,'bold')).pack(anchor='w')
        ttk.Label(top,text='Complete quarter-point answers: B, a and U. Trace setup is included in the total comparison.').pack(anchor='w',pady=(4,8))
        cfg=ttk.LabelFrame(top,text='Inputs and methods',padding=8);cfg.pack(fill='x')
        ttk.Label(cfg,text='Prime grid').grid(row=0,column=0,sticky='w')
        ttk.Combobox(cfg,textvariable=self.mode,values=['paper','geometric','custom'],state='readonly',width=12).grid(row=0,column=1)
        for col,label,var in [(2,'Points',self.count),(4,'Start',self.start),(6,'Factor',self.factor)]:
            ttk.Label(cfg,text=label).grid(row=0,column=col,padx=(10,4));ttk.Entry(cfg,textvariable=var,width=12).grid(row=0,column=col+1)
        ttk.Button(cfg,text='Preview primes',command=self.preview).grid(row=0,column=8,padx=10)
        ttk.Label(cfg,text='Custom primes').grid(row=1,column=0,sticky='w',pady=5)
        ttk.Entry(cfg,textvariable=self.custom,width=85).grid(row=1,column=1,columnspan=8,sticky='ew')
        ttk.Label(cfg,text='Paper: the original 7 primes, then targets 10^9, 10^10, ...; geometric: choose a factor such as 1.5 for denser spacing.').grid(row=2,column=0,columnspan=9,sticky='w')
        method_frame=ttk.Frame(cfg);method_frame.grid(row=3,column=0,columnspan=9,sticky='w',pady=8)
        for i,b in enumerate(METHODS):ttk.Checkbutton(method_frame,text=METHODS[b],variable=self.selected[b]).grid(row=i//2,column=i%2,sticky='w',padx=(0,20))
        ttk.Label(cfg,text='Schoof and point-count BSGS are independent elementary Python backends. Harvey BGS is the C++ recurrence comparator.').grid(row=4,column=0,columnspan=9,sticky='w')
        limits=ttk.Frame(cfg);limits.grid(row=5,column=0,columnspan=9,sticky='w',pady=5)
        for i,b in enumerate(self.maxima):
            ttk.Label(limits,text=b+' max p').grid(row=0,column=i*2,padx=4);ttk.Entry(limits,textvariable=self.maxima[b],width=15).grid(row=0,column=i*2+1)
        timing=ttk.Frame(top);timing.pack(fill='x',pady=8)
        for i,label,var in [(0,'Timing batches',self.reps),(2,'Target ms / batch',self.target),(4,'Deadline s / method / prime',self.timeout),(6,'Model queries Q',self.queries)]:
            ttk.Label(timing,text=label).grid(row=0,column=i,padx=4);ttk.Entry(timing,textvariable=var,width=8).grid(row=0,column=i+1)
        paths=ttk.Frame(top);paths.pack(fill='x')
        for row,label,var,cmd in [(0,'Harvey executable',self.executable,self.choose_exe),(1,'Output folder',self.output,self.choose_output)]:
            ttk.Label(paths,text=label).grid(row=row,column=0,sticky='w');ttk.Entry(paths,textvariable=var,width=100).grid(row=row,column=1,sticky='ew',padx=8,pady=2);ttk.Button(paths,text='Browse',command=cmd).grid(row=row,column=2)
        paths.columnconfigure(1,weight=1)
        buttons=ttk.Frame(top);buttons.pack(fill='x',pady=(8,0))
        self.runbutton=ttk.Button(buttons,text='Run benchmark',command=self.start_run);self.runbutton.pack(side='left')
        self.cancelbutton=ttk.Button(buttons,text='Cancel',command=self.cancel.set,state='disabled');self.cancelbutton.pack(side='left',padx=8)
        ttk.Button(buttons,text='Load previous JSON',command=self.load).pack(side='left')
        ttk.Button(buttons,text='Refresh charts / model Q',command=self.redraw).pack(side='left',padx=8)
        self.status=tk.StringVar(value='Ready. Select extra point counters to compare their preparation costs.');ttk.Label(buttons,textvariable=self.status).pack(side='left',padx=8)
        self.book=ttk.Notebook(root);self.book.pack(fill='both',expand=True,padx=12,pady=(0,12))
        tableframe=ttk.Frame(self.book);self.book.add(tableframe,text='Results table')
        cols=['p','backend','status','prep','query','total','B','a','U']
        self.table=ttk.Treeview(tableframe,columns=cols,show='headings')
        labels=['Prime p','Method','Status','Prep ms','Query ms','Total ms','B mod p','a mod p','U mod p']
        for c,label in zip(cols,labels):self.table.heading(c,text=label);self.table.column(c,width=125 if c!='backend' else 275,stretch=True)
        self.table.grid(row=0,column=0,sticky='nsew')
        scroll=ttk.Scrollbar(tableframe,orient='vertical',command=self.table.yview);scroll.grid(row=0,column=1,sticky='ns')
        horizontal=ttk.Scrollbar(tableframe,orient='horizontal',command=self.table.xview);horizontal.grid(row=1,column=0,columnspan=2,sticky='ew')
        self.table.configure(yscrollcommand=scroll.set,xscrollcommand=horizontal.set);tableframe.rowconfigure(0,weight=1);tableframe.columnconfigure(0,weight=1)
        self.frames={}
        for kind,label in [('total','Complete evaluation'),('preparation','Trace preparation'),('query','Prepared evaluation'),('amortized','Repeated workload model')]:
            f=ttk.Frame(self.book);self.book.add(f,text=label);self.frames[kind]=f
        self.log=tk.Text(root,height=3,wrap='word',state='disabled');self.log.pack(fill='x',padx=12,pady=(0,8),before=self.book)
        self.redraw();root.protocol('WM_DELETE_WINDOW',self.close);root.after(100,self.poll)
    def prime_list(self):return make_primes(self.mode.get(),int(self.count.get()),self.start.get(),self.factor.get(),self.custom.get())
    def preview(self):
        try:messagebox.showinfo('Admissible primes','\n'.join(f'{i+1}: {p:,}' for i,p in enumerate(self.prime_list()))+'\n\nEvery prime is 1 mod 4. 1,000,000,007 is excluded; the first admissible prime >=10⁹ is 1,000,000,009.')
        except Exception as e:messagebox.showerror('Inputs',str(e))
    def choose_exe(self):
        p=filedialog.askopenfilename(title='Choose built Harvey adapter')
        if p:self.executable.set(p)
    def choose_output(self):
        p=filedialog.askdirectory(title='Choose output parent folder')
        if p:self.output.set(str(Path(p)/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')))
    def start_run(self):
        if self.running:return
        try:
            primes=self.prime_list();backends=[b for b in METHODS if self.selected[b].get()]
            if not backends:raise ValueError('Select at least one method.')
            settings=defaults();settings.update(repetitions=int(self.reps.get()),target_ms=float(self.target.get()),timeout=float(self.timeout.get()),executable=self.executable.get(),output=str(Path(self.output.get()).resolve()))
            if not 1<=settings['repetitions']<=100 or not .1<=settings['target_ms']<=1000 or not 1<=settings['timeout']<=86400:raise ValueError('Use 1..100 batches, 0.1..1000 target ms, 1..86400 deadline seconds.')
            for b,v in self.maxima.items():settings[b+'_max_prime']=int(v.get())
            if any((Path(settings['output'])/n).exists() for n in ('summary.csv','benchmark.json')):raise ValueError('Choose a new output folder; this run would overwrite existing results.')
            self.model_q()
        except Exception as e:messagebox.showerror('Inputs',str(e));return
        self.active_output=settings['output'];self.running=True;self.cancel.clear();self.rows=[];self.table.delete(*self.table.get_children());self.redraw()
        self.runbutton.configure(state='disabled');self.cancelbutton.configure(state='normal')
        def work():
            try:
                run_benchmark(primes,backends,settings,self.cancel,self.events.put)
            except Exception as e:self.events.put({'type':'failure','message':str(e)})
        self.run_q=self.model_q();threading.Thread(target=work,daemon=True).start()
    def model_q(self):
        q=int(self.queries.get())
        if not 1<=q<=10**9:raise ValueError('Model Q must be 1..1,000,000,000.')
        return q
    def append_log(self,text):
        self.log.configure(state='normal');self.log.insert('end',text+'\n');self.log.see('end');self.log.configure(state='disabled')
    def add_row(self,r):
        def ms(k):return f'{r[k]:.6g}' if k in r else ''
        self.table.insert('','end',values=[str(r['p']),METHODS[r['backend']],r['status'],ms('prep_median_ms'),ms('query_median_ms'),ms('total_median_ms'),r.get('B_mod_p',''),r.get('a_L_mod_p',''),r.get('U_mod_p','')])
    def poll(self):
        try:
            while True:
                e=self.events.get_nowait();typ=e['type']
                if typ=='progress':self.status.set(e['message'])
                elif typ=='row':
                    self.rows=e['rows'];self.add_row(e['row']);self.append_log(str(e['row']['p'])+' '+e['row']['backend']+': '+e['row']['status']+' '+e['row'].get('message',''))
                elif typ=='done':
                    self.status.set(e['state']+'; saving charts…')
                    try:
                        # All plotting stays on the Tk thread; TkAgg cleanup is not thread-safe.
                        save_charts(self.rows,e['output'],self.run_q);self.redraw()
                        self.append_log('CSV, JSON, PNG and SVG charts saved to '+e['output'])
                        self.status.set(e['state']);self.output.set(fresh_output())
                    except Exception as error:
                        self.status.set('Chart export failed');self.append_log(str(error))
                    self.running=False;self.runbutton.configure(state='normal');self.cancelbutton.configure(state='disabled')
                elif typ in ('saved','failure'):
                    self.running=False;self.runbutton.configure(state='normal');self.cancelbutton.configure(state='disabled');self.status.set('Finished' if typ=='saved' else 'Failed');self.append_log(e['message'])
                    if typ=='saved':self.output.set(fresh_output())
        except queue.Empty:pass
        self.root.after(100,self.poll)
    def redraw(self):
        try:q=self.model_q()
        except ValueError as e:messagebox.showerror('Model',str(e));return
        for kind,f in self.frames.items():
            for child in f.winfo_children():child.destroy()
            with PLOT_LOCK:
                fig=figure_for(self.rows,kind,q);canvas=FigureCanvasTkAgg(fig,master=f);canvas.draw()
            toolbar=NavigationToolbar2Tk(canvas,f,pack_toolbar=False);toolbar.update();toolbar.pack(side='bottom',fill='x')
            canvas.get_tk_widget().pack(side='top',fill='both',expand=True);self.canvases[kind]=canvas
        gc.collect()
    def load(self):
        if self.running:return
        p=filedialog.askopenfilename(filetypes=[('Benchmark JSON','*.json')])
        if not p:return
        try:
            data=json.loads(Path(p).read_text());self.rows=data['rows'];self.table.delete(*self.table.get_children())
            for r in self.rows:self.add_row(r)
            self.redraw();self.append_log('Loaded '+p)
        except Exception as e:messagebox.showerror('Load',str(e))
    def close(self):
        if self.running:
            self.cancel.set();self.status.set('Cancelling; window will close after worker cleanup.')
            self.root.after(200,self.close_when_idle)
        else:self.root.destroy()
    def close_when_idle(self):
        if self.running:self.root.after(200,self.close_when_idle)
        else:self.root.destroy()


def main():
    multiprocessing.freeze_support()
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--headless',action='store_true');ap.add_argument('--mode',choices=['paper','geometric','custom'],default='paper')
    ap.add_argument('--count',type=int,default=7);ap.add_argument('--start',default='97');ap.add_argument('--factor',default='10');ap.add_argument('--primes',default='')
    ap.add_argument('--backends',default='cornacchia,harvey');ap.add_argument('--repetitions',type=int,default=11);ap.add_argument('--target-ms',type=float,default=25)
    ap.add_argument('--timeout',type=float,default=120);ap.add_argument('--executable',default=defaults()['executable']);ap.add_argument('--output',default=fresh_output());ap.add_argument('--queries',type=int,default=1)
    for b in ('harvey','schoof','bsgs'):ap.add_argument('--'+b+'-max-prime',type=int,default=defaults()[b+'_max_prime'])
    args=ap.parse_args()
    if args.headless:
        if not 1<=args.repetitions<=100 or not .1<=args.target_ms<=1000 or not 1<=args.timeout<=86400 or not 1<=args.queries<=10**9:ap.error('Timing or model settings outside supported range')
        backends=args.backends.split(',')
        if any(b not in METHODS for b in backends) or len(set(backends))!=len(backends):ap.error('Use distinct backends from cornacchia,schoof,bsgs,harvey')
        settings=defaults();settings.update(vars(args));settings['target_ms']=args.target_ms
        if (Path(args.output)/'benchmark.json').exists():ap.error('Output already contains a benchmark; use a new directory')
        try:primes=make_primes(args.mode,args.count,args.start,args.factor,args.primes)
        except ValueError as e:ap.error(str(e))
        cancel=threading.Event()
        import signal
        signal.signal(signal.SIGINT,lambda *_:cancel.set())
        rows=run_benchmark(primes,backends,settings,cancel,lambda e:print(e.get('message',e.get('row',{})),flush=True))
        save_charts(rows,args.output,args.queries);print('Saved '+args.output)
    else:
        gui=App(tk.Tk());gui.output.set(args.output);gui.executable.set(args.executable);gui.root.mainloop()

if __name__=='__main__':main()
