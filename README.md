# PG Hostel Management System - 7 Day Learning Plan

This ZIP contains seven progressive, standalone versions of the project.
Each Day_N folder has its own `main.py` and `README.md`.

## Suggested Git workflow
Do the work on the corresponding day, review and test it, then copy that day's `main.py`
to your project working folder (or work directly in one repository using the matching
day's version). Make a real commit when you complete that day's work.

Example commands:
```bash
git add .
git commit -m "Day 1: Create hostel classes and objects"
git push origin main
```

Suggested commit messages:
1. `Day 1: Create Person, Student and Room classes`
2. `Day 2: Add room management`
3. `Day 3: Add student registration`
4. `Day 4: Add room allocation and cancellation`
5. `Day 5: Add student check-in and check-out`
6. `Day 6: Add hostel charges and bill generation`
7. `Day 7: Complete hostel system with TXT file storage and summary`

## Important
- The day folders are progressive learning snapshots, not fabricated Git history.
- Do not create backdated commits or claim you completed work on dates you did not.
- For an authentic GitHub history, implement and understand each day's changes, then commit
  that day's work when you actually finish it.
- Day 7 uses `hostel_data.txt` in the same working directory as `main.py`.
- The data file stores JSON text even though its extension is `.txt`.
- Bills are appended to separate files such as `bill_S101.txt`.
- Python 3 is required. No external packages or database are required.
