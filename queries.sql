SELECT
    d.name AS "Имя",
    d.inn AS "ИНН",
    COUNT(mo.id) AS "TotalSum"
FROM debtors d
JOIN messages m ON d.id = m.debtor_id
JOIN monetary_obligations mo ON m.id = mo.message_id
GROUP BY d.name, d.inn
ORDER BY COUNT(mo.id) DESC
LIMIT 10;
--------------------------------------
SELECT
    d.name AS "Имя",
    d.inn AS "ИНН",
    SUM(mo.debt_sum) AS "DebtSum"
FROM debtors d
JOIN messages m ON d.id = m.debtor_id
JOIN monetary_obligations mo ON m.id = mo.message_id
GROUP BY d.name, d.inn
ORDER BY SUM(mo.debt_sum) DESC
LIMIT 10;
--------------------------------------
SELECT
    d.name AS "Имя",
    d.inn AS "ИНН",
    ROUND(((SUM(mo.total_sum) - SUM(mo.debt_sum)) * 100 / SUM(mo.total_sum))::numeric, 2) AS "RepayPerc"
FROM debtors d
JOIN messages m ON d.id = m.debtor_id
JOIN monetary_obligations mo ON m.id = mo.message_id
GROUP BY d.name, d.inn
ORDER BY "RepayPerc" ASC;