# SPDX-License-Identifier: GPL-2.0-or-later
from pathlib import Path
from threading import RLock
PLOT_LOCK=RLock()
from matplotlib.figure import Figure
from benchmark_engine import METHODS
COLORS={'cornacchia':'#167d9a','schoof':'#c05927','bsgs':'#6c52a3','harvey':'#287b45'}


def figure_for(rows,kind='total',queries=1):
    fig=Figure(figsize=(9,5),dpi=110);ax=fig.add_subplot(111)
    for backend,label in METHODS.items():
        data=sorted((r for r in rows if r['backend']==backend and r['status']=='ok'),key=lambda r:r['p'])
        if kind in ('preparation','query') and backend=='harvey':continue
        field={'total':'total_median_ms','preparation':'prep_median_ms','query':'query_median_ms'}.get(kind)
        if kind=='amortized':
            vals=[r['total_median_ms']*queries if backend=='harvey' else r['prep_median_ms']+queries*r['query_median_ms'] for r in data]
        else:vals=[r.get(field) for r in data]
        pairs=[(r['p'],v) for r,v in zip(data,vals) if v is not None and v>0]
        if pairs:ax.plot([p for p,v in pairs],[v for p,v in pairs],marker='o',markersize=4,label=label,color=COLORS[backend])
    ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Prime p (log scale)')
    ax.set_ylabel('Milliseconds (log scale)');ax.grid(True,which='both',alpha=.2)
    titles={'total':'Complete quarter-point evaluation: preparation + B, a, U',
            'preparation':'Trace preparation only: Cornacchia–Gauss, Schoof, point-count BSGS',
            'query':'Prepared quarter-point evaluation: trace supplied',
            'amortized':f'Illustrative repeated workload: Q = {queries:,}'}
    ax.set_title(titles[kind],fontsize=11)
    if ax.lines:ax.legend(fontsize=8)
    else:ax.text(.5,.5,'No successful measurements yet',transform=ax.transAxes,ha='center')
    foot='Measured medians; elementary Python point counters versus C++ Harvey. Missing results are omitted.'
    if kind=='amortized':foot='Model from measured components: prep + Q × query; Harvey Q × complete. Repeated same quarter-point workload, not Q distinct inputs.'
    fig.text(.02,.015,foot,fontsize=8,wrap=True);fig.tight_layout(rect=(0,.055,1,1))
    return fig


def save_charts(rows,directory,queries=1):
    directory=Path(directory)
    for kind in ('total','preparation','query','amortized'):
        with PLOT_LOCK:
            fig=figure_for(rows,kind,queries)
            fig.savefig(directory/(kind+'.png'),dpi=200)
            fig.savefig(directory/(kind+'.svg'))
            fig.clear()
