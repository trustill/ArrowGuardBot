-- Создаем основную схему
CREATE TABLE users_data (
    user_id BIGINT PRIMARY KEY,
    -- Язык в боте для юзера
    user_lang TEXT,
    accept_tou BOOlEAN,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users_data(user_id),

    plan TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    -- Статус юзера: false - неактивный юзер, true - пользуется услугами
    is_active BOOLEAN,
    -- Активен ли у юзера пробный период
    is_trial BOOLEAN DEFAULT FALSE
);
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,

    user_id BIGINT REFERENCES users_data(user_id),

    plan TEXT,
    status TEXT, -- pending / success / failed

    message_id BIGINT,

    created_at TIMESTAMP DEFAULT NOW(),
    paid_at TIMESTAMP
)