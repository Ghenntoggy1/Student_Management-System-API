from enum import Enum

class RolesEnum(str, Enum):
    admin = 'ADMIN'
    professor = 'PROFESSOR'
    student = 'STUDENT'

class AttendanceStatusEnum(str, Enum):
    present = 'PRESENT'
    late = 'LATE'
    absent = 'ABSENT'

class SessionStatusEnum(str, Enum):
    not_started = 'NOT_STARTED'
    active = 'ACTIVE'
    ended = 'ENDED'
