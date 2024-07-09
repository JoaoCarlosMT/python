import requests
from datetime import datetime
import ctypes

def get_brasilia_time():
    response = requests.get("http://worldtimeapi.org/api/timezone/America/Sao_Paulo")
    data = response.json()
    brasilia_time = data["datetime"]
    return brasilia_time

def update_system_time(hour, minute):
    class SYSTEMTIME(ctypes.Structure):
        _fields_ = [
            ("wYear", ctypes.c_ushort),
            ("wMonth", ctypes.c_ushort),
            ("wDayOfWeek", ctypes.c_ushort),
            ("wDay", ctypes.c_ushort),
            ("wHour", ctypes.c_ushort),
            ("wMinute", ctypes.c_ushort),
            ("wSecond", ctypes.c_ushort),
            ("wMilliseconds", ctypes.c_ushort)
        ]

    now = datetime.now()

    st = SYSTEMTIME()
    st.wYear = now.year
    st.wMonth = now.month
    st.wDay = now.day
    st.wHour = hour
    st.wMinute = minute
    st.wSecond = now.second
    st.wMilliseconds = now.microsecond // 1000

    result = ctypes.windll.kernel32.SetLocalTime(ctypes.byref(st))
    if not result:
        print(f"Falha ao definir a hora do sistema: {ctypes.GetLastError()}")
        return False

    return True

if __name__ == "__main__":
    brasilia_time = get_brasilia_time()
    dt = datetime.fromisoformat(brasilia_time)
    formatted_time = dt.strftime("%H:%M")
    print("Hora de São Paulo:", formatted_time)
    
    hour, minute = map(int, formatted_time.split(':'))

    if update_system_time(hour, minute):
        print("Hora do sistema atualizada com sucesso.")
    else:
        print("Falha ao atualizar a hora do sistema.")
