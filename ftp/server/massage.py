from collections import namedtuple

class Massage:
    process_is_not_over = namedtuple("Process_is_not_over", "status_code masage")
    process_is_not_over = process_is_not_over(status_code = "0", masage ="process is not over")
    process_is_over = namedtuple("Process_is_over","status_code masage")
    process_is_over = process_is_over(status_code = "1", masage ="process is over")
    