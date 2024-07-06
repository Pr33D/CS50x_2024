-- All names
SELECT name
FROM people
WHERE id IN (
    -- All directors
    SELECT person_id
    FROM directors
    WHERE movie_id IN (
        -- All movies
        SELECT movie_id
        FROM ratings
        WHERE rating >= 9.0
    )
)
;
