"""Depth-three family recognition / trace preparation, JSON CLI (A=0 and B=0 seeds).

Examples (run from this directory):
  python cli.py --p 73 --short 4 16
  python cli.py --p 73 --f 1 4 0 37 --trusted-trace 10 --mu 9
  python cli.py --p 73 --f 1 4 0 37 --trusted-trace 10 --verify-sign --mu 9
  python cli.py --p 73 --f 1 4 0 37 --cm --mu 9
  python cli.py --p 73 --short 4 16 --through-depth-two
  python cli.py --p 73 --short 4 16 --verify-certificate cert.json
  python cli.py --p 73 --short 16 27 --family b0
  python cli.py --p 73 --f 1 60 0 10 --family b0 --cm --mu 17
--family a0 (default) is the A=0-seed family (discriminant -192, p = 1 mod 24);
--family b0 is the B=0-seed family (discriminant -256, p = x^2 + 64 y^2), whose
trace is exact by Ireland & Rosen Ch. 18 Theorem 5.
A supplied trace is trusted apart from the Hasse interval and the family's
necessary condition 4p-t^2=192f^2; --verify-sign checks its sign. --cm
computes the trace itself (Cornacchia candidates plus a sign rule) and needs
no supplied trace. The default sign rule is deterministic: Ireland & Rosen
(1990) Ch. 18 Theorem 4 applied to the j=0 seed. --sign-method las_vegas uses
the zero-error point test instead; its retry cap is 64 raw x draws by default,
--unbounded-sign-test runs the almost-surely terminating variant with <=5
expected raw trials, and a capped attempt may report trace_sign_inconclusive.
"""
import argparse
import json
from dataclasses import asdict
from depth_three_recognize import (recognize_depth_three, recognize_short_through_depth_three,
                                   prepare_from_trace, prepare_cm, verify_supplied_certificate,
                                   RecognizedPreparation, CMPreparation)
from depth_three_b0_recognize import (recognize_depth_three_b0, prepare_from_trace_b0, prepare_cm_b0,
                                      verify_supplied_certificate_b0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--p', type=int, required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--short', type=int, nargs=2, metavar=('A', 'B'))
    g.add_argument('--f', type=int, nargs=4, metavar=('ONE', 'C', 'B', 'A'))
    p.add_argument('--trusted-trace', type=int)
    p.add_argument('--verify-sign', action='store_true', help='check the supplied trace (deterministic by default)')
    p.add_argument('--cm', action='store_true', help='compute the trace by Cornacchia plus a sign rule')
    p.add_argument('--sign-method', choices=['sextic', 'las_vegas'], default='sextic',
                   help='sign rule: deterministic Ireland-Rosen Thm 4 (a0) / Thm 5 (b0) by default, or the point test')
    p.add_argument('--family', choices=['a0', 'b0'], default='a0', help='depth-three family: A=0 seed (a0) or B=0 seed (b0)')
    p.add_argument('--mu', type=int)
    p.add_argument('--through-depth-two', action='store_true', help='also run the retained depth<=2 recognizer')
    p.add_argument('--verify-certificate', metavar='JSON', help='reverify a stored certificate for --short')
    retries = p.add_mutually_exclusive_group()
    retries.add_argument('--max-sign-trials', type=int, default=64, help='positive raw-x trial cap (default 64)')
    retries.add_argument('--unbounded-sign-test', action='store_true', help='repeat until a conclusive witness; <=5 expected raw trials')
    args = p.parse_args()
    try:
        max_trials = None if args.unbounded_sign_test else args.max_sign_trials
        if max_trials is not None and max_trials <= 0:
            raise ValueError('--max-sign-trials must be positive')
        if args.cm and args.trusted_trace is not None:
            raise ValueError('choose --cm or --trusted-trace')
        if args.short is not None:
            if args.verify_certificate:
                with open(args.verify_certificate) as handle:
                    verifier = verify_supplied_certificate_b0 if args.family == 'b0' else verify_supplied_certificate
                    out = verifier(args.p, *args.short, json.load(handle))
            elif args.through_depth_two:
                out = recognize_short_through_depth_three(*args.short, args.p)
            elif args.family == 'b0':
                out = recognize_depth_three_b0(*args.short, args.p)
            else:
                out = recognize_depth_three(*args.short, args.p)
        else:
            if args.family == 'b0':
                if args.cm:
                    ev = prepare_cm_b0(args.p, args.f, sign_method='las_vegas' if args.sign_method == 'las_vegas' else 'quartic',
                                       max_trials=max_trials)
                elif args.trusted_trace is None:
                    raise ValueError('--f preparation requires --trusted-trace or --cm')
                else:
                    ev = prepare_from_trace_b0(args.p, args.f, args.trusted_trace, verify_trace=args.verify_sign)
            elif args.cm:
                ev = prepare_cm(args.p, args.f, max_trials=max_trials, sign_method=args.sign_method)
            elif args.trusted_trace is None:
                raise ValueError('--f preparation requires --trusted-trace or --cm')
            else:
                ev = prepare_from_trace(args.p, args.f, args.trusted_trace, verify_sign=(args.sign_method if args.verify_sign else False), max_trials=max_trials)
            if isinstance(ev, (RecognizedPreparation, CMPreparation)):
                out = asdict(ev)
                out['status'] = 'prepared_by_cm_trace' if isinstance(ev, CMPreparation) else 'prepared_from_caller_trusted_trace'
                if isinstance(ev, RecognizedPreparation) and args.verify_sign:
                    out['status'] = 'prepared_from_sign_verified_trace'
                if args.mu is not None:
                    out['query'] = ev.evaluator.query(args.mu)
            else:
                out = ev
    except (ValueError, KeyError) as err:
        out = {'status': 'invalid_input', 'error': str(err)}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
