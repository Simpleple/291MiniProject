select distinct tickets.tno, tickets.name, to_char(bookings.dep_date), 
    flight_fares.price
    from bookings, tickets, flight_fares, passengers
    where passengers.email = 'davood@ggg.com'
    and tickets.name = passengers.name
    and bookings.tno = tickets.tno
    and flight_fares.fare = bookings.fare
    and flight_fares.flightno = bookings.flightno;
