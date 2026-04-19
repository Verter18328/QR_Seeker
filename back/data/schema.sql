CREATE TYPE question_type AS ENUM ('single', 'multi', 'text');

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    token VARCHAR(64) UNIQUE NOT NULL,
    points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE qr_codes (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE NOT NULL,
    label VARCHAR(200),
    has_quiz BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    qr_id INT NOT NULL REFERENCES qr_codes(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type question_type NOT NULL DEFAULT 'single',
    points INT NOT NULL DEFAULT 1,
    sort_order INT NOT NULL DEFAULT 0
);

CREATE TABLE quiz_options (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE scans (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    qr_id INT NOT NULL REFERENCES qr_codes(id) ON DELETE CASCADE,
    scanned_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(player_id, qr_id)
);

CREATE TABLE quiz_answers (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    question_id INT NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
    selected_options JSONB,
    text_answer TEXT,
    is_correct BOOLEAN NOT NULL DEFAULT false,
    answered_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(player_id, question_id)
);
