import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(r'c:/Users/user/Agentic AI Projects/.env'))
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
prompt = {
    'aggregated_positions': {
        'cash_positions': [
            {'account_id': 'acct-001', 'currency': 'USD', 'balance': 4500000.0, 'timestamp': '2026-08-06T12:00:00'},
            {'account_id': 'acct-002', 'currency': 'EUR', 'balance': 2800000.0, 'timestamp': '2026-08-06T12:00:00'},
        ],
        'nostro_by_currency': {'USD': 3900000.0, 'EUR': 1800000.0, 'GBP': 960000.0},
        'funding_gaps': [{'account_id': 'acct-001', 'obligations_due': 5000000.0, 'available_liquidity': 4500000.0, 'timestamp': '2026-08-06T12:00:00'}],
        'collateral_movements': [],
        'settlement_timeline': [],
        'market_indicators': [],
    },
    'forecast': {'shortfall_projected': True, 'amount': 500000.0, 'currency': 'USD', 'estimated_time_to_breach_minutes': 120, 'rationale': 'test'},
    'active_alerts': [{'metric': 'funding_gap', 'account': 'acct-002', 'threshold': 100000.0, 'actual_value': 1000000.0}],
}
system = 'Write a short governance commentary using only provided figures. Mention the forecast and active alerts clearly.'
user = json.dumps(prompt)
print('sending...', len(user))
try:
    r = client.chat.completions.create(
        model='gpt-4o-mini',
        response_format={'type': 'json_object'},
        messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        timeout=60,
    )
    print(r.choices[0].message.content)
except Exception as e:
    import traceback
    traceback.print_exc()
