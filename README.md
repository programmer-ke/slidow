# slidow

Virtual interactions

### How it works

- Moderator creates an event (extend: with duration specified)
- Adds a quiz type interaction
- Names the quiz
- Adds questions to quiz
  - For each
    - Add options
	- select correct option(s)
- Launches quiz
- Waits for at least one participant to join
  - for each question
    - Sends question
	- Collect responses (extend: within time limit)
	- Reveals answer and grades each participant
- Closes quiz
- Reveals leaderboard
- Closes event

# Todo

- [x] add black + mypy
- [x] figure out mypy and tests setup 
- [x] modify domain to have non-optional child attributes
- [ ] integrate sqlalchemy, flask and get a web ui
  - [x] add orm tests following recipe: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
  - [ ] fix mypy hanging
