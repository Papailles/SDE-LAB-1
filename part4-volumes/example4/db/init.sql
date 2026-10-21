CREATE TABLE IF NOT EXISTS bookings (
    id         SERIAL PRIMARY KEY,
    student    TEXT        NOT NULL,
    exam_id    INTEGER     NOT NULL,
    course     TEXT        NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
