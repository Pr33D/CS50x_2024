-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Facts: July, 28, 2023 Humphrey Street


-- MISSION: Check the reports of the day
SELECT description
FROM crime_scene_reports
WHERE year = 2023
AND month = 7
AND day = 28
AND street = 'Humphrey Street'
;
-- Theft took place at 10:15am, bakery


-- MISSION: Review interviews
SELECT name, transcript
FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28
AND transcript LIKE '%bakery%'
;


-- Ruth said, the thief took a car after the theft
-- MISSION: Figure out, who left the parking lot after the theft
SELECT people.name
FROM bakery_security_logs
JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25
AND activity = 'exit'
;

-- Eugene said, he saw the thief at the atm in leggett street earlier, withdrawing some money
    -- He said, it was someone he recognizes...
-- MISSION: Figure out, who used the atm in leggett street on that day
SELECT people.name
FROM atm_transactions
JOIN people ON people.id = (
    SELECT person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number = atm_transactions.account_number
)
WHERE year = 2023
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
;

-- Raymond said, he heard the thief calling someone for less than a minute and asking for
    -- the other one to buy flight tickets for
    -- the earliest flight on the other day
-- MISSION: Check calls of that day
SELECT people.name
FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60
;

-- MISSION: Find Passengers on earliest flight of Juli, 29
SELECT name
FROM people
WHERE passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id IN (
        SELECT id
        FROM flights
        WHERE year = 2023
        AND month = 7
        AND day = 29
        AND origin_airport_id IN (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville'
        )
        ORDER BY hour, minute LIMIT 1
    )
)
;


-- MISSION: Combine everything to 1 Query and find the thief
SELECT name
FROM people
WHERE name IN (
    SELECT people.name
    FROM bakery_security_logs
    JOIN people ON bakery_security_logs.license_plate = people.license_plate
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity = 'exit'
)
AND name IN (
    SELECT people.name
    FROM atm_transactions
    JOIN people ON people.id = (
    SELECT person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number = atm_transactions.account_number
    )
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
)
AND name IN (
    SELECT people.name
    FROM phone_calls
    JOIN people ON phone_calls.caller = people.phone_number
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration < 60
)
AND name IN (
    SELECT name
    FROM people
    WHERE passport_number IN (
        SELECT passport_number
        FROM passengers
        WHERE flight_id IN (
            SELECT id
            FROM flights
            WHERE year = 2023
            AND month = 7
            AND day = 29
            AND origin_airport_id IN (
                SELECT id
                FROM airports
                WHERE city = 'Fiftyville'
            )
            ORDER BY hour, minute LIMIT 1
        )
    )
)
;
-- Bruce stole the duck!


-- MISSION: Find his accomplice by checking the calls again
SELECT people.name
FROM phone_calls
JOIN people ON phone_calls.receiver = people.phone_number
WHERE caller = (
    SELECT phone_number
    FROM people
    WHERE name = 'Bruce'
)
AND year = 2023
AND month = 7
AND day = 28
AND duration < 60
;
-- Robin was the only one Bruce called -> He must be his accomplice!


-- MISSION: Find city Bruce escaped to
SELECT city
FROM airports
WHERE id IN (
    SELECT destination_airport_id
    FROM flights
    WHERE id IN (
        SELECT flight_id
        FROM passengers
        WHERE passport_number IN (
            SELECT passport_number
            FROM people
            WHERE name = 'Bruce'
        )
    )
)
;
-- He escaped to New York City!
-- Now, lets catch him there ;)
