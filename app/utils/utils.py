from datetime import datetime, time, timedelta



def round_time_to_half_hour(dt: datetime) -> time:
    # Dodajemy 15 minut, aby "przeskoczyć" próg zaokrąglania
    # a następnie dzielimy czas na bloki 30-minutowe
    rounded_dt = dt + timedelta(minutes=15)
    minute = (rounded_dt.minute // 30) * 30
    
    # Obsługa przypadku, gdy zaokrąglenie minut przesuwa nas na kolejną godzinę
    # (np. 15:45 -> 16:00)
    return time(rounded_dt.hour, minute)
