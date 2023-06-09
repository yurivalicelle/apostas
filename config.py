# config.py
class Configuration:
    instance = None

    class __Configuration:
        def __init__(self):
            self.TELEGRAM_TOKEN = "6022257134:AAFZLma2Z1S6oz0jeivjJWz6cpWwaVvHEUg"
            self.CHAT_ID = "-964640871"
            self.HEADERS = {
                'authority': 'scores24.live',
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/json',
                'cookie': 'userOddFormat=EU; machineTimezone=GMT-3; scores24_anon=eyJpdiI6InZtSDlheHliWFp1XC9heG43ZURUODl3PT0iLCJ2YWx1ZSI6IlwvXC9SVnE2Wm56Z01vUStSMnI2YVh2dGVOQ29idk50aDJGaEJIWUhGcW1SaGdBc1RtTzJBbUpuUUxjNnFCK0c5cFlpakVzeXJxa3ZGWklcL1hZVGd6MzNrN1doS1FlczAxSGtrUThXWTFxM0FzPSIsIm1hYyI6ImUxYWRiYTQ2ZjZlZWUwMjgxYjI5ZjY5M2I1NDVjYmNlZmE3MjViYjlmNGE2YWQxYWYzYjFlZTVhMWZkNGE1NmUifQ%3D%3D; cookiesAccepted=1; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlJ2THFlaktzZFBsV1F4Z2hxeFRKdVE9PSIsInZhbHVlIjoiNHFhZCtwRkp5ZnpKM1MwWEVFYnNRTlwvTitrbWRTV0lwVSt2SDZJMnBjcFMzMDBRVzREdG9TME1vb2VtSjV6Nno2bFJESXRNaFd6Sm45amJvdE9MdXFnN041ODA2a0IzMjV2aGIwM0NodDUwWk1ZS1ZhTGFzM2JSZDZBYnpONHNSRmVIZzQ1cDBPM1RLekw3T09JZU1mdkE1bnVIUk1KRE0yWTRMaVFRWWpHWnBLZlwvbEp0U2d1ZG1HUzZPQlFNNDBscDNRcGRUOW9KS0tQTkdTaldXT1k0aWZ3NXpvblM4eDA4NkFVMWU5VmhkeFpFb2FFNWhBQ3pTQ1FXY2xJSXlwIiwibWFjIjoiMmE1Mjk2MzAzNjg3M2JmNWY0YmE5MjM5NTVkNDgwOTFmYzdlMzdmNzJlMzc2MGVjYmVkYWNkMmQxODY0Njk4OCJ9; auth=1; latestWidth=1536; 2d4d6=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wic3RyZWFtc1wiOntcIjEwMTA2XCI6MTY4MDY0NTM1NSxcIjIxNDNcIjoxNjgwNzI5NzU3LFwiMTAyNTRcIjoxNjgwNzI5NzczfSxcImNhbXBhaWduc1wiOntcIjkyXCI6MTY4MDY0NTM1NSxcIjg1XCI6MTY4MDcyOTc1NyxcIjEwNFwiOjE2ODA3Mjk3NzN9LFwidGltZVwiOjE2ODA2NDUzNTV9In0.B80mkXEEXgfrYTQSgwUlrAr_3hS4RDQYrQsK5PCMqkA; _token=uuid_s3ddd21jusruk_s3ddd21jusruk642de6b26d38a5.61969538; language=en; _subid=h9iena1k9lvg8; s24-session=6WXTLSNVojHPStYj490xP5cJ7QzPVpFH3i3Z8FaY; io=KnsJOVAmh782w6CHbGtt; promoPopupClosed=2; promo-proxy-2d4d6=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wic3RyZWFtc1wiOntcIjY3NDNcIjoxNjgxMTI1MTQyLFwiMjMxN1wiOjE2ODExMjUxNjYsXCIyMzc2XCI6MTY4MTAzNDI0NSxcIjIzMzRcIjoxNjgxMTI1MTY2fSxcImNhbXBhaWduc1wiOntcIjEyMFwiOjE2ODExMjUxNDIsXCI4NlwiOjE2ODEwNTI1MDksXCI1NVwiOjE2ODEwMDkyMTksXCI5NVwiOjE2ODExMjUxNjYsXCI2MlwiOjE2ODEwMzQyNDUsXCI0NVwiOjE2ODExMjUxNjZ9LFwidGltZVwiOjE2ODExMjUxNDJ9In0.vl2eRMr9KhheAQHlV7QyBOnB-tofS_THcpy6qCTXln4; promo-proxy-_subid=s3ddd21kcg9nf; promo-proxy-_token=uuid_s3ddd21kcg9nf_s3ddd21kcg9nf6433ef48d97205.44026509; s24-session=6WXTLSNVojHPStYj490xP5cJ7QzPVpFH3i3Z8FaY',
                'origin': 'https://scores24.live',
                'referer': 'https://scores24.live/en/trends/tennis',
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'x-bot-identifier': 'client',
                'x-country': 'br',
                'x-ssr-ip': '189.107.108.247',
                'x-user-cache': '2VDsCIpHskUxRyPahDHB',
                'x-user-ip': '189.107.108.247'
            }
            self.OPERATION_NAME = "TrendsTopQuery"
            self.QUERY_STRING = "query TrendsTopQuery($lang: String, $timezoneOffset: Int, $sportSlug: String!) {\n  TrendsTopQuery(lang: $lang, timezone_offset: $timezoneOffset, sport_slug: $sportSlug) {\n id\n    facts\n    match {\n      langSlug: lang_slug\n      sportSlug: sport_slug\n      slug\n      matchDate: match_date\n      teams {\n        logo\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    prediction {\n      value\n      type\n      __typename\n    }\n    bookmaker {\n      logo\n      slug\n      name\n      color\n      legal\n      url\n      __typename\n    }\n    __typename\n  }\n}\n"
            self.OPERATION_NAME_PREDICTION = "PredictionsSports"
            self.QUERY_STRING_PREDICTION = "query PredictionsSports($sportSlugs: [String!], $lang: String!, $timezoneOffset: Int, $limit: Int, $skip: Int, $topMatches: Boolean, $day: DayEnum!) {\n  TopPredictionsQuery(sport_slug: $sportSlugs, lang: $lang, timezone_offset: $timezoneOffset, limit: $limit, skip: $skip, top_matches: $topMatches, day: $day) {\n    items {\n      ...PredictionsCardFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PredictionsCardFragment on CachedPrediction {\n  prediction\n  predictionValue: prediction_value\n  match {\n    slug\n    uniqueTournament: unique_tournament {\n      name\n      __typename\n    }\n    sportSlug: sport_slug\n    matchDate: match_date\n    country {\n      iso\n      slug\n      __typename\n    }\n    teams {\n      name\n      logo\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n"
            self.QUERY_STRING_PREDICTION_FACT = "query MatchPrediction($matchSlug: String!, $langSlug: String!, $sportSlug: String!) {\n  GeneratedPrediction(match_slug: $matchSlug, lang: $langSlug, sport_slug: $sportSlug) {\n    text {\n      teams\n      teamsCompose {\n        last10\n        last365\n        __typename\n      }\n      intro\n      h2h\n      prediction\n      trends\n      oddsCalc\n      standing\n      bracket\n      statsCompare\n      __typename\n    }\n    createdDate: created_date\n    prediction\n    predictionValue: prediction_value\n    __typename\n  }\n}\n"
            self.OPERATION_NAME_PREDICTION_FACT = "MatchPrediction"

    def __new__(cls):
        if not Configuration.instance:
            Configuration.instance = Configuration.__Configuration()
        return Configuration.instance
