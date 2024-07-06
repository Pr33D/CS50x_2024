SELECT COUNT(*)
FROM movies
JOIN ratings on movie_id = movies.id
WHERE rating = 10.0;
