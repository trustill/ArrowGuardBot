-- Создаем основную схему
CREATE TABLE users_data(
    user_id BIGINT PRIMARY KEY,
    -- Язык в боте для юзера
    user_lang TEXT,
    -- Статус юзера: 0 - неактивный юзер, 1 - пользуется услугами
    user_status INTEGER,
    -- Активен ли у юзера пробный период
    is_trial BOOlEAN,
    accept_tou BOOlEAN,
    end_sub DATE
)