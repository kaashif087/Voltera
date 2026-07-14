"""
VOLTERA Recommendation Priority Manager

This module determines the importance of multiple
battery situations and selects the highest priority
recommendation.

Priority Order:

CRITICAL
    ↓
HIGH
    ↓
MEDIUM
    ↓
LOW

Input:
    List of detected battery situations

Output:
    Highest priority situation
"""