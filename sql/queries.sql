SELECT id, title, price FROM excursions ORDER BY title;

SELECT * FROM excursions WHERE price < 2000;

SELECT * FROM bookings WHERE is_cancelled = 0;

SELECT * FROM excursions ORDER BY price DESC;

SELECT bookings.id, excursions.title, bookings.date 
FROM bookings 
JOIN excursions ON bookings.excursion_id = excursions.id;

SELECT bookings.id, excursions.title, bookings.date 
FROM bookings 
JOIN excursions ON bookings.excursion_id = excursions.id 
WHERE bookings.is_cancelled = 0;

SELECT COUNT(*) AS total FROM excursions;

SELECT AVG(price) AS avg_price FROM excursions;

SELECT excursions.title, COUNT(bookings.id) AS count_bookings 
FROM excursions 
LEFT JOIN bookings ON excursions.id = bookings.excursion_id 
GROUP BY excursions.id;

SELECT excursions.title, COUNT(bookings.id) AS count_bookings 
FROM excursions 
JOIN bookings ON excursions.id = bookings.excursion_id 
GROUP BY excursions.id 
HAVING COUNT(bookings.id) > 0;