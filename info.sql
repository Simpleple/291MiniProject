select tickets.name, tickets.email, tickets.paid_price, flight_fares.price, fares.fare, fares.descr, flight_fares.bag_allow, bookings.flightno, bookings.seat, bookings.dep_date, to_char(flights.dep_time, 'HH24:MI'), flights.est_dur, flights.src, a1.name, a1.city, a1.country, a1.tzone, flights.dst, a2.name, a2.city, a2.country, a2.tzone
from tickets, flight_fares, fares, bookings, flights, airports a1, airports a2
where tickets.tno = 111
and bookings.tno = tickets.tno
and flight_fares.fare = bookings.fare
and flight_fares.flightno = bookings.flightno
and fares.fare = flight_fares.fare
and flights.flightno = bookings.flightno
and a1.acode = flights.src
and a2.acode = flights.dst;
