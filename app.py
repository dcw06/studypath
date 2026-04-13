from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import threading
import time
import webbrowser
import json as _json_mod
import game_db
import resources as res_db
import math_gen

# pywebview is only available in the desktop build — import it optionally
try:
    import webview
    _WEBVIEW_AVAILABLE = True
except ImportError:
    _WEBVIEW_AVAILABLE = False

load_dotenv()

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip, enumerate=enumerate)
game_db.init_db()
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
# SERVER_NAME must only be set in local desktop mode; on a real host it breaks routing
if os.getenv('FLASK_ENV') == 'desktop':
    app.config['SERVER_NAME'] = 'localhost:5002'

oauth = OAuth(app)

# ── OAuth Providers ────────────────────────────────────────────────────────────

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

facebook = oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_APP_ID'),
    client_secret=os.getenv('FACEBOOK_APP_SECRET'),
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)

microsoft = oauth.register(
    name='microsoft',
    client_id=os.getenv('MICROSOFT_CLIENT_ID'),
    client_secret=os.getenv('MICROSOFT_CLIENT_SECRET'),
    server_metadata_url=f'https://login.microsoftonline.com/{os.getenv("MICROSOFT_TENANT_ID", "common")}/v2.0/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

wechat = oauth.register(
    name='wechat',
    client_id=os.getenv('WECHAT_APP_ID'),
    client_secret=os.getenv('WECHAT_APP_SECRET'),
    access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token',
    authorize_url='https://open.weixin.qq.com/connect/qrconnect',
    api_base_url='https://api.weixin.qq.com/',
    client_kwargs={'scope': 'snsapi_login'},
)

# Providers with known issues (mirrors the warning shown in the UI)
UNAVAILABLE_PROVIDERS = {'microsoft', 'wechat'}

# ── i18n ───────────────────────────────────────────────────────────────────────

LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Español',
    'zh': '中文',
    'tl': 'Filipino',
    'vi': 'Tiếng Việt',
}

TRANSLATIONS = {
    'en': {
        'sign_in': 'Sign In',
        'create_account': 'Create Account',
        'sign_in_to_continue': 'Sign in to continue',
        'subtitle': 'Enter your email or choose a provider below',
        'email': 'Email',
        'password': 'Password',
        'or_continue_with': 'or continue with',
        'provider_unavailable': 'You are currently unable to log in with Microsoft, WeChat. We are working on this.',
        'encrypted_auth': 'All sign-in methods use encrypted, verified authentication',
        'already_have_account': 'You already have an account. Please sign in below.',
        'apply': 'Apply',
        'invalid_credentials': 'Invalid email or password.',
        'full_name': 'Full Name',
        'confirm_password': 'Confirm Password',
        'create_account_btn': 'Create Account',
        'passwords_no_match': 'Passwords do not match.',
        'account_created': 'Account created! Please sign in.',
    },
    'es': {
        'sign_in': 'Iniciar sesión',
        'create_account': 'Crear cuenta',
        'sign_in_to_continue': 'Inicia sesión para continuar',
        'subtitle': 'Ingresa tu correo o elige un proveedor abajo',
        'email': 'Correo electrónico',
        'password': 'Contraseña',
        'or_continue_with': 'o continuar con',
        'provider_unavailable': 'Actualmente no puedes iniciar sesión con Microsoft, WeChat. Estamos trabajando en ello.',
        'encrypted_auth': 'Todos los métodos usan autenticación encriptada y verificada',
        'already_have_account': 'Ya tienes una cuenta. Por favor inicia sesión.',
        'apply': 'Aplicar',
        'invalid_credentials': 'Correo o contraseña incorrectos.',
        'full_name': 'Nombre completo',
        'confirm_password': 'Confirmar contraseña',
        'create_account_btn': 'Crear cuenta',
        'passwords_no_match': 'Las contraseñas no coinciden.',
        'account_created': '¡Cuenta creada! Por favor inicia sesión.',
    },
    'zh': {
        'sign_in': '登录',
        'create_account': '创建账户',
        'sign_in_to_continue': '登录以继续',
        'subtitle': '输入您的电子邮件或选择以下提供商',
        'email': '电子邮件',
        'password': '密码',
        'or_continue_with': '或继续使用',
        'provider_unavailable': '您目前无法使用 Microsoft、WeChat 登录，我们正在处理此问题。',
        'encrypted_auth': '所有登录方式均使用加密验证',
        'already_have_account': '您已有账户，请在下方登录。',
        'apply': '应用',
        'invalid_credentials': '邮箱或密码错误。',
        'full_name': '姓名',
        'confirm_password': '确认密码',
        'create_account_btn': '创建账户',
        'passwords_no_match': '两次密码不一致。',
        'account_created': '账户已创建！请登录。',
    },
    'tl': {
        'sign_in': 'Mag-sign In',
        'create_account': 'Lumikha ng Account',
        'sign_in_to_continue': 'Mag-sign in upang magpatuloy',
        'subtitle': 'Ilagay ang iyong email o pumili ng provider sa ibaba',
        'email': 'Email',
        'password': 'Password',
        'or_continue_with': 'o magpatuloy gamit ang',
        'provider_unavailable': 'Hindi ka makapag-log in gamit ang Microsoft, WeChat ngayon. Nag-aayos kami nito.',
        'encrypted_auth': 'Lahat ng paraan ng pag-sign in ay gumagamit ng naka-encrypt na pag-verify',
        'already_have_account': 'Mayroon ka nang account. Mangyaring mag-sign in sa ibaba.',
        'apply': 'Ilapat',
        'invalid_credentials': 'Maling email o password.',
        'full_name': 'Buong Pangalan',
        'confirm_password': 'Kumpirmahin ang Password',
        'create_account_btn': 'Lumikha ng Account',
        'passwords_no_match': 'Hindi magkatugma ang mga password.',
        'account_created': 'Nagawa na ang account! Mangyaring mag-sign in.',
    },
    'vi': {
        'sign_in': 'Đăng nhập',
        'create_account': 'Tạo tài khoản',
        'sign_in_to_continue': 'Đăng nhập để tiếp tục',
        'subtitle': 'Nhập email của bạn hoặc chọn nhà cung cấp bên dưới',
        'email': 'Email',
        'password': 'Mật khẩu',
        'or_continue_with': 'hoặc tiếp tục với',
        'provider_unavailable': 'Hiện tại bạn không thể đăng nhập bằng Microsoft, WeChat. Chúng tôi đang xử lý.',
        'encrypted_auth': 'Tất cả phương thức đăng nhập đều sử dụng xác thực được mã hóa',
        'already_have_account': 'Bạn đã có tài khoản. Vui lòng đăng nhập bên dưới.',
        'apply': 'Áp dụng',
        'invalid_credentials': 'Email hoặc mật khẩu không đúng.',
        'full_name': 'Họ và tên',
        'confirm_password': 'Xác nhận mật khẩu',
        'create_account_btn': 'Tạo tài khoản',
        'passwords_no_match': 'Mật khẩu không khớp.',
        'account_created': 'Tài khoản đã được tạo! Vui lòng đăng nhập.',
    },
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def get_lang():
    return request.args.get('lang', session.get('lang', 'en'))

def t(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    lang = get_lang()
    session['lang'] = lang
    error = None
    success = request.args.get('success')

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'apply_lang':
            lang = request.form.get('language', 'en')
            session['lang'] = lang
            return redirect(url_for('login', lang=lang))

        if action == 'signin':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            # TODO: replace with real DB lookup
            if email and password:
                session['user'] = {'email': email}
                return redirect(url_for('dashboard'))
            error = t(lang)['invalid_credentials']

    return render_template(
        'login.html',
        t=t(lang),
        lang=lang,
        languages=LANGUAGE_NAMES,
        error=error,
        success=success,
        tab='signin',
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = get_lang()
    session['lang'] = lang
    error = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'apply_lang':
            lang = request.form.get('language', 'en')
            session['lang'] = lang
            return redirect(url_for('register', lang=lang))

        if action == 'register':
            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')
            if password != confirm:
                error = t(lang)['passwords_no_match']
            else:
                # TODO: save user to DB
                return redirect(url_for('login', success='1', lang=lang))

    return render_template(
        'login.html',
        t=t(lang),
        lang=lang,
        languages=LANGUAGE_NAMES,
        error=error,
        success=None,
        tab='register',
    )

# ── OAuth Login ────────────────────────────────────────────────────────────────

# Providers that must open in the system browser (Google blocks embedded WebView)
BROWSER_PROVIDERS = {'google'}

# Server-side store: maps oauth state → authlib token params
# Used so the callback works even when it arrives in a different browser
import secrets as _secrets
_pending_oauth: dict = {}   # { state: {'nonce': ..., 'code_verifier': ...} }
_completed_oauth: dict = {} # { state: email }  — written by callback, read by /check


@app.route('/auth/<provider>')
def oauth_login(provider):
    if provider in UNAVAILABLE_PROVIDERS:
        return redirect(url_for('login', lang=get_lang()))
    client = oauth.create_client(provider)
    redirect_uri = url_for('oauth_callback', provider=provider, _external=True)

    if provider in BROWSER_PROVIDERS:
        # Build the auth URL; returns a dict with url/state/nonce
        auth_data = client.create_authorization_url(redirect_uri)
        state = auth_data['state']
        nonce = auth_data.get('nonce', '')
        _pending_oauth[state] = {'nonce': nonce}
        session['oauth_state'] = state  # used by /check to poll for completion

        webbrowser.open(auth_data['url'])
        return render_template('waiting.html', provider=provider.title())

    return client.authorize_redirect(redirect_uri)


@app.route('/auth/<provider>/check')
def oauth_check(provider):
    """Polled by the waiting page — redirects to dashboard once callback completes."""
    state = session.get('oauth_state')
    if state and state in _completed_oauth:
        email = _completed_oauth.pop(state)
        session['user'] = {'email': email, 'provider': provider}
        session.pop('oauth_state', None)
        return redirect(url_for('dashboard'))
    return render_template('waiting.html', provider=provider.title())


@app.route('/auth/<provider>/callback')
def oauth_callback(provider):
    client = oauth.create_client(provider)

    if provider in BROWSER_PROVIDERS:
        # Callback arrives in system browser — exchange code manually (no session needed)
        state = request.args.get('state', '')
        code  = request.args.get('code', '')
        pending = _pending_oauth.pop(state, {})
        nonce = pending.get('nonce', '')
        redirect_uri = url_for('oauth_callback', provider=provider, _external=True)

        import requests as _requests
        token_resp = _requests.post('https://oauth2.googleapis.com/token', data={
            'code':          code,
            'client_id':     os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri':  redirect_uri,
            'grant_type':    'authorization_code',
        }).json()

        id_token = token_resp.get('id_token', '')
        # Decode payload without verifying signature (already came from Google)
        import base64, json as _json
        try:
            payload_b64 = id_token.split('.')[1]
            payload_b64 += '=' * (-len(payload_b64) % 4)
            user_info = _json.loads(base64.urlsafe_b64decode(payload_b64))
            email = user_info.get('email')
        except Exception:
            email = None

        if email and state:
            _completed_oauth[state] = email

        return """<html><head><meta charset="utf-8"></head>
        <body style="text-align:center;margin-top:80px;font-family:-apple-system,Arial">
        <h2 style="color:#1a3a8f">&#10003; Signed in successfully!</h2>
        <p>You can close this tab and return to the app.</p>
        <script>setTimeout(function(){window.close();},2000);</script>
        </body></html>"""

    # Non-browser providers (Facebook, GitHub, Microsoft)
    lang = session.get('lang', 'en')
    token = client.authorize_access_token()

    if provider == 'facebook':
        resp = client.get('me?fields=id,name,email')
        email = resp.json().get('email')
    elif provider == 'github':
        resp = client.get('user')
        info = resp.json()
        email = info.get('email')
        if not email:
            # Email is private — fetch from /user/emails and use primary verified one
            emails_resp = client.get('user/emails')
            emails = emails_resp.json() if isinstance(emails_resp.json(), list) else []
            primary = next((e for e in emails if e.get('primary') and e.get('verified')), None)
            email = primary['email'] if primary else None
    elif provider == 'microsoft':
        user_info = token.get('userinfo') or client.userinfo()
        email = user_info.get('email') or user_info.get('preferred_username')
    else:
        email = None

    if email:
        session['user'] = {'email': email, 'provider': provider}
        return redirect(url_for('dashboard'))
    return redirect(url_for('login', lang=lang))

# ── Protected / API ────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return redirect(url_for('game_dashboard'))


# ── Game helpers ───────────────────────────────────────────────────────────────

def _require_player():
    """Return the current player dict, or None if not logged in."""
    user = session.get('user')
    if not user:
        return None
    email = user.get('email', 'guest@quizarena.local')
    player = game_db.get_or_create_player(email)
    session['player_id'] = player['id']
    return player

def _get_stats(player_id):
    sessions = game_db.get_player_sessions(player_id, limit=1000)
    games = len(sessions)
    if games == 0:
        return {'games_played': 0, 'avg_score': 0, 'total_correct': 0}
    total_correct = sum(s['score'] for s in sessions)
    total_q = sum(s['total'] for s in sessions) or 1
    return {
        'games_played': games,
        'avg_score': round(total_correct / total_q * 100),
        'total_correct': total_correct,
    }

def _get_rank(player_id):
    lb = game_db.get_leaderboard(limit=1000)
    for i, p in enumerate(lb, 1):
        if p['id'] == player_id:
            return i
    return len(lb) + 1


# ── Game Routes ────────────────────────────────────────────────────────────────

@app.route('/game')
def game_home():
    player = _require_player()
    leaderboard = game_db.get_leaderboard(limit=5)
    daily = game_db.get_daily_challenge()
    with game_db.get_db() as _db:
        total_questions = _db.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    subjects = game_db.get_subjects()
    return render_template('game_home.html', active='home', leaderboard=leaderboard,
                           player=player, daily=daily,
                           total_questions=total_questions,
                           total_subjects=len(subjects))


@app.route('/game/dashboard')
def game_dashboard():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    stats = _get_stats(player['id'])
    rank = _get_rank(player['id'])
    recent = game_db.get_player_sessions(player['id'], limit=5)
    daily = game_db.get_daily_challenge()
    subjects = game_db.get_subjects()
    mastery = game_db.get_subject_mastery(player['id'])

    # Last session for "continue playing" card
    all_sessions = game_db.get_player_sessions(player['id'], limit=1)
    last_session = all_sessions[0] if all_sessions else None

    # Daily done check
    today = __import__('datetime').date.today().isoformat()
    daily_done = any(
        s.get('mode') == 'daily' and s.get('created_at', '')[:10] == today
        for s in recent
    )

    # Recommend subjects/topics the player hasn't tried recently
    recent_subjects = {s['subject'] for s in recent if s.get('subject')}
    recommended = []
    for subj in subjects:
        if subj not in recent_subjects:
            topics = game_db.get_topics(subj)
            if topics:
                recommended.append((subj, topics[0]))
        if len(recommended) >= 3:
            break

    league_progress = game_db.get_league_progress(player['xp'])
    return render_template('game_dashboard.html', active='dashboard',
                           player=player, stats=stats, rank=rank,
                           recent_sessions=recent, daily=daily,
                           subjects=subjects,
                           subject_meta=game_db.SUBJECT_META,
                           mastery=mastery,
                           last_session=last_session,
                           daily_done=daily_done,
                           recommended=recommended,
                           league_progress=league_progress,
                           notifications=[])


@app.route('/game/modes')
def game_modes():
    player = _require_player()
    return render_template('game_modes.html', active='modes', player=player)


@app.route('/game/topics')
def game_topics():
    player = _require_player()
    mode = request.args.get('mode', 'solo')
    subject = request.args.get('subject', '')
    topics = game_db.get_topics(subject) if subject else []
    subjects = game_db.get_subjects()

    # Recent topics from last 10 sessions
    recent_topics = []
    if player:
        recent_sessions = game_db.get_player_sessions(player['id'], limit=10)
        seen = set()
        for s in recent_sessions:
            key = (s.get('subject', ''), s.get('topic', ''))
            if key not in seen and key[0]:
                seen.add(key)
                recent_topics.append(key)
        recent_topics = recent_topics[:5]

    return render_template('game_topics.html', active='modes', player=player,
                           mode=mode,
                           selected_subject=subject,
                           selected_topic='',
                           selected_diff='medium',
                           topics=topics,
                           subjects=subjects,
                           subject_meta=game_db.SUBJECT_META,
                           subject_meta_json=_json_mod.dumps(game_db.SUBJECT_META),
                           subject_resources_json=_json_mod.dumps(res_db.SUBJECT_RESOURCES),
                           platforms_json=_json_mod.dumps(res_db.PLATFORMS),
                           recent_topics=recent_topics)


@app.route('/game/topics-for/<subject>')
def game_topics_for(subject):
    topics = game_db.get_topics(subject)
    return jsonify({'topics': topics})


@app.route('/game/lobby/setup', methods=['POST'])
def game_lobby_setup():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    mode       = request.form.get('mode', 'solo')
    subject    = request.form.get('subject', '')
    topic      = request.form.get('topic', '')
    difficulty = request.form.get('difficulty', 'medium')
    count      = int(request.form.get('count', 10))
    return redirect(url_for('game_lobby', mode=mode, subject=subject,
                            topic=topic, difficulty=difficulty, count=count))


@app.route('/game/lobby')
def game_lobby():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    mode       = request.args.get('mode', 'solo')
    subject    = request.args.get('subject', '')
    topic      = request.args.get('topic', '')
    difficulty = request.args.get('difficulty', 'medium')
    count      = int(request.args.get('count', 10))

    # Daily challenge overrides
    if mode == 'daily':
        daily = game_db.get_daily_challenge()
        subject = daily.get('subject', 'Math')
        topic = daily.get('topic', '')
        count = 5

    return render_template('game_lobby.html', active='modes', player=player,
                           mode=mode, subject=subject, topic=topic,
                           difficulty=difficulty, count=count)


@app.route('/game/start', methods=['POST'])
def game_start():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    mode       = request.form.get('mode', 'solo')
    subject    = request.form.get('subject', '')
    topic_raw  = request.form.get('topic', '')
    difficulty = request.form.get('difficulty', 'medium')
    count      = int(request.form.get('count', 10))

    # Resolve random topic
    topic = topic_raw
    if topic_raw == 'random' or not topic_raw:
        topics = game_db.get_topics(subject) if subject else []
        import random
        topic = random.choice(topics) if topics else ''

    # Daily challenge: load fixed question IDs
    questions = []
    procedural = False
    if mode == 'daily':
        daily = game_db.get_daily_challenge()
        ids = _json_mod.loads(daily.get('question_ids', '[]'))
        with game_db.get_db() as db:
            rows = db.execute(
                "SELECT * FROM questions WHERE id IN ({})".format(','.join('?' * len(ids))),
                ids
            ).fetchall()
            for r in rows:
                q = dict(r)
                q['choices'] = _json_mod.loads(q['choices'])
                questions.append(q)
    elif subject == 'Math':
        # Generate fresh random questions at runtime for Math
        questions = math_gen.generate_for_topic(
            topic=topic or 'Arithmetic',
            difficulty=difficulty,
            count=count
        )
        procedural = True
    else:
        questions = game_db.get_questions(
            subject=subject or None,
            topic=topic or None,
            difficulty=difficulty,
            limit=count
        )

    if not questions:
        # Fallback: ignore filters
        questions = game_db.get_questions(limit=count)

    session_id = game_db.create_session(player['id'], mode, subject, topic, difficulty)
    session['game_questions'] = [q['id'] for q in questions]
    # For procedural questions, store full data (no DB IDs to look up later)
    if procedural:
        session['game_questions_data'] = questions
    else:
        session.pop('game_questions_data', None)
    session['game_session_id'] = session_id

    return render_template('game_play.html', active='modes', player=player,
                           questions=questions,
                           questions_json=_json_mod.dumps(questions),
                           session_id=session_id,
                           session_data={
                               'mode': mode, 'subject': subject,
                               'difficulty': difficulty, 'count': len(questions)
                           })


@app.route('/game/submit', methods=['POST'])
def game_submit():
    data = request.get_json()
    session_id  = data.get('session_id')
    answers     = data.get('answers', [])
    score       = data.get('score', 0)
    time_taken  = data.get('time_taken', 0)

    gs = game_db.get_session(session_id)
    if not gs:
        return jsonify({'redirect': url_for('game_modes')}), 400

    total = len(answers)
    mode  = gs['mode']
    xp_per = {'solo':10,'practice':8,'timed':15,'survival':20,'daily':50,'blitz':25,'bot':18,'ranked':30}.get(mode, 10)
    xp_earned = score * xp_per
    if mode == 'daily' and score == total:
        xp_earned += 50  # completion bonus

    player_id = gs['player_id']
    rank_before = _get_rank(player_id)

    game_db.complete_session(session_id, score, total, xp_earned, time_taken, answers)
    game_db.add_xp(player_id, xp_earned)

    rank_after = _get_rank(player_id)

    # Store for results page
    session['last_session_id'] = session_id
    session['last_answers']    = answers
    session['rank_before']     = rank_before
    session['rank_after']      = rank_after
    session['last_time_taken'] = time_taken
    return jsonify({'redirect': url_for('game_results', sid=session_id)})


@app.route('/game/autosave', methods=['POST'])
def game_autosave():
    """Called via sendBeacon when the user closes/navigates away mid-game."""
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id')
    answers    = data.get('answers', [])
    score      = data.get('score', 0)
    time_taken = data.get('time_taken', 0)

    if not session_id:
        return '', 204

    gs = game_db.get_session(session_id)
    if not gs or gs.get('completed'):
        return '', 204   # already saved or invalid

    total = len(answers) if answers else 0
    mode  = gs.get('mode', 'solo')
    xp_per = {'solo':10,'practice':8,'timed':15,'survival':20,'daily':50,'blitz':25,'bot':18,'ranked':30}.get(mode, 10)
    xp_earned = score * xp_per

    game_db.complete_session(session_id, score, total, xp_earned, time_taken, answers)
    game_db.add_xp(gs['player_id'], xp_earned)
    return '', 204


@app.route('/game/results')
def game_results():
    player = _require_player()
    sid = request.args.get('sid', type=int)
    gs  = game_db.get_session(sid) if sid else None
    if not gs:
        return redirect(url_for('game_modes'))

    # Reload questions for review
    given = session.get('last_answers', [])
    questions = []
    proc_data = session.get('game_questions_data')
    if proc_data:
        # Procedurally generated questions — already full dicts, no DB lookup needed
        questions = proc_data
    else:
        q_ids = session.get('game_questions', [])
        if q_ids:
            with game_db.get_db() as db:
                rows = db.execute(
                    "SELECT * FROM questions WHERE id IN ({})".format(','.join('?' * len(q_ids))),
                    q_ids
                ).fetchall()
                id_map = {r['id']: dict(r) for r in rows}
                for qid in q_ids:
                    if qid in id_map:
                        q = id_map[qid]
                        q['choices'] = _json_mod.loads(q['choices'])
                        questions.append(q)

    total = gs['total'] or 1
    pct = round(gs['score'] / total * 100)

    rank_before = session.get('rank_before')
    rank_after  = session.get('rank_after')
    secs = session.get('last_time_taken', 0)
    time_str = f"{secs // 60}m {secs % 60}s" if secs >= 60 else f"{secs}s"

    # Build per-topic resources for "Learn More" links on missed questions
    missed_topics = set()
    for i, q in enumerate(questions):
        given_ans = given[i] if i < len(given) else -1
        if given_ans != q.get('answer'):
            missed_topics.add(q.get('topic', ''))
    topic_resources = {
        topic: res_db.get_resources_for_topic(gs.get('subject', ''), topic)
        for topic in missed_topics if topic
    }

    return render_template('game_results.html', active='modes', player=player,
                           gs=gs, pct=pct, questions=questions,
                           given_answers=given,
                           rank_before=rank_before, rank_after=rank_after,
                           time_str=time_str,
                           topic_resources=topic_resources,
                           platforms=res_db.PLATFORMS)


@app.route('/game/leaderboard')
def game_leaderboard():
    player = _require_player()
    current_id = player['id'] if player else None
    period  = request.args.get('period', 'all')
    subject = request.args.get('subject', '')

    # Filter leaderboard by period and/or subject using sessions
    if period == 'all' and not subject:
        players = game_db.get_leaderboard(limit=50)
    else:
        import datetime as _dt
        cutoff = None
        if period == 'weekly':
            cutoff = (_dt.date.today() - _dt.timedelta(days=7)).isoformat()
        elif period == 'monthly':
            cutoff = (_dt.date.today() - _dt.timedelta(days=30)).isoformat()
        sql = """
            SELECT p.id, p.username, p.avatar, p.level,
                   COALESCE(SUM(s.xp_earned),0) AS xp,
                   COUNT(s.id) AS games_played
            FROM players p
            LEFT JOIN game_sessions s ON s.player_id=p.id AND s.completed=1
        """
        params = []
        wheres = []
        if cutoff:
            wheres.append("s.created_at >= ?"); params.append(cutoff)
        if subject:
            wheres.append("s.subject=?"); params.append(subject)
        if wheres:
            sql += " WHERE " + " AND ".join(wheres)
        sql += " GROUP BY p.id ORDER BY xp DESC LIMIT 50"
        with game_db.get_db() as _db:
            players = [dict(r) for r in _db.execute(sql, params).fetchall()]

    # Find current player's rank in this filtered list
    my_rank = None
    my_player = None
    if current_id:
        for i, p in enumerate(players, 1):
            if p['id'] == current_id:
                my_rank = i
                my_player = p
                break
        if my_player is None:
            my_player = player

    subjects = game_db.get_subjects()
    return render_template('game_leaderboard.html', active='leaderboard',
                           player=player, players=players,
                           current_player_id=current_id,
                           current_period=period,
                           current_subject=subject,
                           my_rank=my_rank, my_player=my_player,
                           subjects=subjects,
                           subject_meta=game_db.SUBJECT_META)


@app.route('/game/profile', methods=['GET', 'POST'])
def game_profile():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    username_error = None
    if request.method == 'POST':
        avatar = request.form.get('avatar')
        if avatar:
            game_db.update_player(player['id'], avatar=avatar)
            player = game_db.get_player(player['id'])
        elif request.form.get('action') == 'username':
            new_name = request.form.get('username', '').strip()
            if 2 <= len(new_name) <= 24:
                try:
                    game_db.update_player(player['id'], username=new_name)
                    player = game_db.get_player(player['id'])
                except Exception:
                    username_error = 'That username is already taken.'
            else:
                username_error = 'Username must be 2–24 characters.'
    stats = _get_stats(player['id'])
    rank = _get_rank(player['id'])
    recent = game_db.get_player_sessions(player['id'], limit=10)
    mastery = game_db.get_subject_mastery(player['id'])
    achievements = game_db.get_player_achievements(player['id'])
    league_progress = game_db.get_league_progress(player['xp'])
    return render_template('game_profile.html', active='profile', player=player,
                           stats=stats, rank=rank, recent_sessions=recent,
                           mastery=mastery, achievements=achievements,
                           subject_meta=game_db.SUBJECT_META,
                           league_progress=league_progress,
                           username_error=username_error)


@app.route('/game/settings', methods=['GET', 'POST'])
def game_settings():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    default_prefs = {
        'default_difficulty': 'medium',
        'default_count': 10,
        'show_explanations': True,
        'sound_effects': False,
        'music': False,
        'daily_reminder': True,
        'rank_alerts': False,
        'language': 'en',
        'large_text': False,
        'reduce_motion': False,
        'colorblind': False,
        'timer_extra': 0,
        'public_profile': True,
        'share_activity': False,
    }
    prefs = {**default_prefs, **session.get('prefs', {})}
    saved = False
    if request.method == 'POST':
        prefs['default_difficulty'] = request.form.get('default_difficulty', 'medium')
        prefs['default_count']      = int(request.form.get('default_count', 10))
        prefs['show_explanations']  = bool(request.form.get('show_explanations'))
        prefs['sound_effects']      = bool(request.form.get('sound_effects'))
        prefs['music']              = bool(request.form.get('music'))
        prefs['daily_reminder']     = bool(request.form.get('daily_reminder'))
        prefs['rank_alerts']        = bool(request.form.get('rank_alerts'))
        prefs['language']           = request.form.get('language', 'en')
        prefs['large_text']         = bool(request.form.get('large_text'))
        prefs['reduce_motion']      = bool(request.form.get('reduce_motion'))
        prefs['colorblind']         = bool(request.form.get('colorblind'))
        prefs['timer_extra']        = int(request.form.get('timer_extra', 0))
        prefs['public_profile']     = bool(request.form.get('public_profile'))
        prefs['share_activity']     = bool(request.form.get('share_activity'))
        # Role update
        new_role = request.form.get('role')
        if new_role in ('student', 'teacher', 'parent'):
            game_db.update_player(player['id'], role=new_role)
            player = game_db.get_player(player['id'])
        session['prefs'] = prefs
        saved = True
    return render_template('game_settings.html', active='settings',
                           player=player, prefs=prefs, saved=saved)


@app.route('/game/reset-progress', methods=['POST'])
def game_reset_progress():
    player = _require_player()
    if not player:
        return redirect(url_for('login'))
    game_db.update_player(player['id'], xp=0, level=1, streak=0)
    with game_db.get_db() as db:
        db.execute("DELETE FROM game_sessions WHERE player_id=?", (player['id'],))
    return redirect(url_for('game_settings'))

@app.route('/game/leagues')
@app.route('/game/leagues/<league_id>')
def game_leagues(league_id=None):
    player = _require_player()
    xp = player['xp'] if player else 0

    league_progress = game_db.get_league_progress(xp)
    all_leagues = game_db.LEAGUES

    # Which league tab to show — default to the player's current league
    active_league_id = league_id or league_progress['current']['id']
    active_league = next((lg for lg in all_leagues if lg['id'] == active_league_id), all_leagues[0])
    members = game_db.get_league_members(active_league_id)

    # Attach progress info to every league for the overview display
    leagues_with_status = []
    for lg in all_leagues:
        nxt = next((l for l in all_leagues if l['min_xp'] > lg['min_xp']), None)
        tier_size = (nxt['min_xp'] - lg['min_xp']) if nxt else None
        leagues_with_status.append({
            **lg,
            'tier_size': tier_size,
            'unlocked': xp >= lg['min_xp'],
            'is_current': lg['id'] == league_progress['current']['id'],
        })

    return render_template('game_leagues.html', active='leagues',
                           player=player,
                           league_progress=league_progress,
                           all_leagues=leagues_with_status,
                           active_league=active_league,
                           members=members)


@app.route('/game/resources')
def game_resources():
    player = _require_player()
    subjects = game_db.get_subjects()

    # Build topic_resources[subj][topic] = [res, ...]
    topic_resources = {}
    topic_counts = {}
    for subj in subjects:
        topic_resources[subj] = {}
        total = 0
        for topic in game_db.get_topics(subj):
            rs = res_db.TOPIC_RESOURCES.get(topic, [])
            if rs:
                topic_resources[subj][topic] = rs
                total += len(rs)
        topic_counts[subj] = total

    # Curated interactive tools
    tools = [
        {"title": "Desmos Graphing Calculator", "url": "https://www.desmos.com/calculator",     "platform": "desmos",    "icon": "📈", "desc": "Plot functions, inequalities, and more in real time."},
        {"title": "Desmos Scientific Calculator","url": "https://www.desmos.com/scientific",    "platform": "desmos",    "icon": "🧮", "desc": "Full-featured scientific calculator in your browser."},
        {"title": "Wolfram Alpha",               "url": "https://www.wolframalpha.com",         "platform": "wolfram",   "icon": "🔢", "desc": "Solve equations, compute derivatives, look up facts."},
        {"title": "Wolfram ODE Solver",          "url": "https://www.wolframalpha.com/calculators/ode-calculator/","platform":"wolfram","icon":"∂","desc":"Step-by-step ODE solutions."},
        {"title": "Wolfram Matrix Calculator",   "url": "https://www.wolframalpha.com/calculators/matrix-calculator/","platform":"wolfram","icon":"[M]","desc":"Determinants, inverses, eigenvalues."},
        {"title": "PhET Simulations",            "url": "https://phet.colorado.edu",            "platform": "wolfram",   "icon": "⚛️", "desc": "Interactive science & math simulations from CU Boulder."},
        {"title": "GeoGebra",                    "url": "https://www.geogebra.org",             "platform": "desmos",    "icon": "📐", "desc": "Geometry, algebra, statistics & calculus tools."},
        {"title": "Periodic Table (Ptable)",     "url": "https://ptable.com",                   "platform": "wolfram",   "icon": "⚗️", "desc": "Interactive periodic table with trends and properties."},
        {"title": "VisuAlgo",                    "url": "https://visualgo.net",                 "platform": "wolfram",   "icon": "🔗", "desc": "Animated visualizations of data structures & algorithms."},
        {"title": "SQLZoo",                      "url": "https://sqlzoo.net",                   "platform": "wolfram",   "icon": "🗄️", "desc": "Interactive SQL tutorials with live query execution."},
        {"title": "Purdue OWL",                  "url": "https://owl.purdue.edu",               "platform": "coursera",  "icon": "✍️", "desc": "Authoritative writing & grammar guides from Purdue."},
        {"title": "Investopedia",                "url": "https://www.investopedia.com",         "platform": "wikipedia", "icon": "💰", "desc": "Economics and finance definitions, tutorials, examples."},
    ]

    return render_template('game_resources.html', active='resources',
                           player=player,
                           subjects=subjects,
                           subject_meta=game_db.SUBJECT_META,
                           subject_resources=res_db.SUBJECT_RESOURCES,
                           topic_resources=topic_resources,
                           topic_counts=topic_counts,
                           platforms=res_db.PLATFORMS,
                           tools=tools)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/status')
def api_status():
    return jsonify({'status': 'ok', 'authenticated': 'user' in session})

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/data-deletion', methods=['GET', 'POST'])
def data_deletion():
    confirmation_code = None
    if request.method == 'POST':
        import secrets as _s
        # TODO: queue actual deletion job for the submitted email
        confirmation_code = _s.token_hex(8).upper()
    return render_template('data_deletion.html', confirmation_code=confirmation_code)

@app.route('/facebook/data-deletion', methods=['POST'])
def facebook_data_deletion():
    """
    Facebook calls this endpoint with a signed_request when a user
    removes the app from their Facebook settings.
    Must return JSON with a URL where users can check deletion status.
    """
    import base64, hashlib, hmac, json as _json
    signed_request = request.form.get('signed_request', '')
    app_secret = os.getenv('FACEBOOK_APP_SECRET', '').encode()

    try:
        encoded_sig, payload = signed_request.split('.', 1)
        sig = base64.urlsafe_b64decode(encoded_sig + '==')
        expected = hmac.new(app_secret, payload.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            return jsonify({'error': 'Invalid signature'}), 400
        data = _json.loads(base64.urlsafe_b64decode(payload + '=='))
        user_id = data.get('user_id', 'unknown')
    except Exception:
        user_id = 'unknown'

    # TODO: queue deletion of all data associated with this Facebook user_id
    import secrets as _s
    confirmation_code = _s.token_hex(8).upper()
    status_url = url_for('data_deletion', _external=True) + f'?code={confirmation_code}'
    return jsonify({'url': status_url, 'confirmation_code': confirmation_code})

# ── Run ────────────────────────────────────────────────────────────────────────

PORT = 5002

if __name__ == '__main__':
    if _WEBVIEW_AVAILABLE and os.getenv('FLASK_ENV') != 'production':
        # Desktop mode — wrap in a native window
        os.environ.setdefault('FLASK_ENV', 'desktop')

        def _run_flask():
            app.run(host='localhost', port=PORT, debug=False, use_reloader=False, threaded=True)

        threading.Thread(target=_run_flask, daemon=True).start()
        time.sleep(1)  # wait for Flask to bind

        def _on_closed():
            with game_db.get_db() as db:
                open_sessions = db.execute(
                    "SELECT id, player_id, mode FROM game_sessions WHERE completed=0"
                ).fetchall()
                for row in open_sessions:
                    sid = row['id']
                    db.execute(
                        "UPDATE game_sessions SET completed=1, score=COALESCE(score,0), "
                        "total=COALESCE(total,0), xp_earned=COALESCE(xp_earned,0), "
                        "time_taken=COALESCE(time_taken,0) WHERE id=?",
                        (sid,)
                    )

        window = webview.create_window(
            title='StudyPath',
            url=f'http://localhost:{PORT}/',
            width=560,
            height=820,
            resizable=True,
            min_size=(480, 600),
        )
        webview.start(func=None)
    else:
        # Plain web server mode (used by gunicorn in production too)
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', PORT)), debug=False)
    _on_closed()
