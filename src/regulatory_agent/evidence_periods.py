"""Explicit source intervals are statements, not proof of coverage or control operation."""
import csv
from datetime import datetime
from io import StringIO
import re

from .contracts import Citation, EvidencePeriod

MONTH = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
DATE = rf'(?:\d{{4}}-\d{{2}}-\d{{2}}|\d{{1,2}}\s+{MONTH}\s+\d{{4}}|{MONTH}\s+\d{{1,2}},?\s+\d{{4}})'
INTERVAL = re.compile(rf'(?<!\w)(?P<start>{DATE})\s*(?:\bto\b|\bthrough\b|\buntil\b|[-–—])\s*(?P<end>{DATE})(?!\w)', re.I)


def _date(value):
    text = ' '.join(value.replace(',', ' ').split())
    for format in ('%Y-%m-%d', '%d %B %Y', '%d %b %Y', '%B %d %Y', '%b %d %Y'):
        try: return datetime.strptime(text, format).date().isoformat()
        except ValueError: pass
    raise ValueError('unknown_evidence_date')


def _citation(passage, quote=None):
    return Citation(**{k:passage[k] for k in ('document_version_id','passage_id','location')},
                    quote=passage['text'] if quote is None else quote).model_dump()


def with_periods(source):
    """Return derived metadata without changing the saved source or trusting an outer period field."""
    result = {k:v for k,v in source.items() if k != 'evidence_period'} | {'stated_periods':[]}
    if source['document']['kind'] != 'evidence': return result
    passages = source['passages']
    if source.get('format') == 'csv':
        try:
            rows = [next(csv.reader(StringIO(p['text']), strict=True)) for p in passages]
            names = [name.strip().lower().replace(' ', '_').replace('-', '_') for name in rows[0]]
            starts = [i for i,n in enumerate(names) if n in {'period_start','evidence_period_start'}]
            ends = [i for i,n in enumerate(names) if n in {'period_end','evidence_period_end'}]
            if len(starts) != 1 or len(ends) != 1: return result
            for passage,row in zip(passages[1:],rows[1:]):
                if len(row) != len(names): continue
                try: period = EvidencePeriod(start=_date(row[starts[0]]),end=_date(row[ends[0]]))
                except ValueError: continue
                result['stated_periods'].append({'period':period.model_dump(),
                    'citations':[_citation(passages[0]),_citation(passage)]})
        except (csv.Error, StopIteration, IndexError): pass
        return result
    for passage in passages:
        matches = list(INTERVAL.finditer(passage['text']))
        if not matches: continue
        try:
            periods = [EvidencePeriod(start=_date(m['start']),end=_date(m['end'])) for m in matches]
        except ValueError: continue
        if len({(p.start,p.end) for p in periods}) != 1: continue
        result['stated_periods'].append({'period':periods[0].model_dump(),
            'citations':[_citation(passage,matches[0].group())]})
    return result
