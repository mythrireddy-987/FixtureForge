# First-Order Logic (FOL) Rules for FixtureForge

## Predicates

- Team(x): x is a team.
- Match(x): x is a match.
- Venue(x): x is a venue.
- Plays(x,y): Team x participates in match y.
- Scheduled(y): Match y has been scheduled.
- AssignedVenue(y,v): Match y is assigned to venue v.
- Available(v): Venue v is available.
- ValidDate(y): Match y has a valid date.
- SameTime(x,y): Matches x and y have the same time.
- SameDate(x,y): Matches x and y have the same date.
- SameVenue(x,y): Matches x and y use the same venue.
- RestViolation(x,y): Matches x and y violate the minimum rest requirement.
- Conflict(x,y): Matches x and y have a scheduling conflict.

## 15 FOL Sentences and Interpretations

1. ∀x (Team(x) → Team(x))

   Interpretation: Every team is recognised as a team.

2. ∀x (Match(x) → Match(x))

   Interpretation: Every match is recognised as a match.

3. ∀x (Venue(x) → Venue(x))

   Interpretation: Every venue is recognised as a venue.

4. ∀m (Scheduled(m) → Match(m))

   Interpretation: Every scheduled item must be a match.

5. ∀m (Scheduled(m) → ValidDate(m))

   Interpretation: Every scheduled match must have a valid date.

6. ∀m (Scheduled(m) → ∃v (Venue(v) ∧ AssignedVenue(m,v)))

   Interpretation: Every scheduled match must be assigned a venue.

7. ∀m∀v (AssignedVenue(m,v) → Available(v))

   Interpretation: A match can only be assigned to an available venue.

8. ∀m∀t (Plays(t,m) → Team(t))

   Interpretation: Every participant in a match must be a team.

9. ∀m (Match(m) → ∃t1∃t2 (Team(t1) ∧ Team(t2) ∧ Plays(t1,m) ∧ Plays(t2,m)))

   Interpretation: Every match must involve two teams.

10. ∀x∀y ((SameDate(x,y) ∧ SameTime(x,y) ∧ SameVenue(x,y)) → Conflict(x,y))

    Interpretation: Two matches at the same venue, date and time create a conflict.

11. ∀x∀y (RestViolation(x,y) → Conflict(x,y))

    Interpretation: A violation of the minimum rest requirement creates a conflict.

12. ∀x∀y (Conflict(x,y) → ¬(Scheduled(x) ∧ Scheduled(y)))

    Interpretation: Two conflicting matches cannot both be scheduled.

13. ∀m (Scheduled(m) → ∃v AssignedVenue(m,v))

    Interpretation: Every scheduled match must have an assigned venue.

14. ∀m (Scheduled(m) → ValidDate(m))

    Interpretation: A scheduled match must have a valid date.

15. ∀x∀y ((Scheduled(x) ∧ Scheduled(y) ∧ Conflict(x,y)) → ¬(Scheduled(x) ∧ Scheduled(y)))

    Interpretation: Conflicting matches cannot both be included in the final schedule.