% FIXTUREFORGE - LEAGUE RULES KNOWLEDGE BASE

% 1. Teams
team(rcb).
team(csk).
team(mi).
team(kkr).

% 2. Venues
venue(stadium_a).
venue(stadium_b).

% 3. Available venues
available(stadium_a).
available(stadium_b).

% 4. Matches
match(m1).
match(m2).
match(m3).
match(m4).
match(m5).
match(m6).

% 5. Teams participating in matches
plays(rcb, m1).
plays(csk, m1).

plays(rcb, m2).
plays(mi, m2).

plays(rcb, m3).
plays(kkr, m3).

plays(csk, m4).
plays(mi, m4).

plays(csk, m5).
plays(kkr, m5).

plays(mi, m6).
plays(kkr, m6).

% 6. Match scheduling information
schedule(m1, 1, 10, stadium_a).
schedule(m2, 3, 10, stadium_a).
schedule(m3, 5, 10, stadium_a).
schedule(m4, 5, 14, stadium_b).
schedule(m5, 7, 10, stadium_b).
schedule(m6, 7, 14, stadium_a).

% RULES

% Rule 1: Every scheduled match must be a valid match.
scheduled(M) :-
    schedule(M, _, _, _),
    match(M).

% Rule 2: Every match must involve exactly two participating teams.
two_teams(M) :-
    plays(T1, M),
    plays(T2, M),
    T1 \= T2,
    \+ (plays(T3, M), T3 \= T1, T3 \= T2).

% Rule 3: A scheduled match must use an available venue.
valid_venue(M) :-
    schedule(M, _, _, V),
    available(V).

% Rule 4: Two matches conflict if they use the same venue,
% date and time.
venue_conflict(M1, M2) :-
    schedule(M1, D, T, V),
    schedule(M2, D, T, V),
    M1 \= M2.

% Rule 5: Two matches share a team.
shared_team(M1, M2) :-
    plays(Team, M1),
    plays(Team, M2),
    M1 \= M2.

% Rule 6: Two matches violate the rest requirement
% if a common team has less than two days of rest.
rest_violation(M1, M2) :-
    schedule(M1, D1, _, _),
    schedule(M2, D2, _, _),
    shared_team(M1, M2),
    Difference is abs(D1 - D2),
    Difference < 2.

% Rule 7: A fixture is valid if its venue is available.
valid_fixture(M) :-
    scheduled(M),
    valid_venue(M),
    two_teams(M).

% Rule 8: A schedule has no venue conflict.
no_venue_conflict(M1, M2) :-
    \+ venue_conflict(M1, M2).

% Rule 9: A schedule has no rest violation.
sufficient_rest(M1, M2) :-
    \+ rest_violation(M1, M2).

% Rule 10: A match is assigned to a venue.
assigned_venue(M, V) :-
    schedule(M, _, _, V),
    venue(V).

% Rule 11: A team participates in a match.
participating_team(T, M) :-
    team(T),
    plays(T, M).

% Rule 12: A match is scheduled on a particular day.
scheduled_on(M, D) :-
    schedule(M, D, _, _).

% Rule 13: A match is scheduled at a particular time.
scheduled_at(M, T) :-
    schedule(M, _, T, _).

% Rule 14: A match uses a particular venue.
played_at(M, V) :-
    schedule(M, _, _, V).

% Rule 15: A match is valid when it satisfies all basic rules.
valid_match(M) :-
    valid_fixture(M).