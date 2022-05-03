from typing import Tuple
import logging
from datetime import datetime


class GetStipend:
    @classmethod
    def get_stipend(cls, raw_text: str) -> Tuple[int, int]:
        if "Unpaid" in raw_text:
            monthly_stipend = 0
            weekly_stipend = 0
            return monthly_stipend, weekly_stipend
        elif " /month" in raw_text:
            monthly_stipend = cls._parse_stipend("".join(raw_text.strip().split(" /month")))
            return monthly_stipend, 0
        elif " /week" not in raw_text and "Unpaid" not in raw_text:
            monthly_stipend = cls._parse_stipend(raw_text)
            return monthly_stipend, 0
        elif " /week" in raw_text:
            weekly_stipend = cls._parse_stipend("".join(raw_text.strip().split(" /week")))
            return 0, weekly_stipend
        else:
            logging.info(datetime, raw_text)

    @staticmethod
    def _parse_stipend(stipend: str) -> int:
        if len(stipend) < 6:
            return int(stipend)
        elif len(stipend) > 5:
            if "-" in stipend and " lump sum" in stipend:
                raw_stipend = stipend.split(" lump sum")
                raw_stipend = raw_stipend[0].split("-")
                avg = (int(raw_stipend[0]) + int(raw_stipend[1])) // 2
                return int(avg)
            elif "-" in stipend:
                stipend = list(map(int, stipend.split("-")))
                avg = (stipend[0] + stipend[1]) // 2
                return int(avg)
            elif " lump sum +  Incentives" in stipend:
                stipend = "".join(stipend.split(" lump sum +  Incentives"))
                return int(stipend)
            elif " +  Incentives" in stipend:
                stipend = "".join(stipend.split(" +  Incentives"))
                return int(stipend)
            elif " lump sum" in stipend:
                stipend = "".join(stipend.split(" lump sum"))
                return int(stipend)
            else:
                logging.info(datetime, stipend)
