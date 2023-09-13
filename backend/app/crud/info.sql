SELECT
    report."create",
    count(DISTINCT report.post_id) AS rsum,
    count(DISTINCT report.browser_id) AS bsum,
    count(DISTINCT report.taboola_id) AS tsum
FROM
    report
GROUP BY
    CURRENT_DATE(report."create")