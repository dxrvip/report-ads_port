select
    t.id,
    count(distinct p.id),
    count(distinct r.id),
    count(distinct r.visitor_ip),
    sum(
        case
            when r.is_page then 1
            else 0
        end
    ) / count(distinct p.id) as count_post_id,
    count(distinct bi.id),
    count(distinct p2.id)
from
    taboola t
    join post_taboola_table ptt on ptt.taboola_id = t.id
    join post p on p.id = ptt.post_id
    join report r on r.taboola_id = t.id
    join browser_info bi on bi.id = r.browser_id
    join post_browser_table pbt on bi.id = pbt.browser_id
    join post p2 on pbt.post_id = p2.id
    join (
        select
            t2.id
        from
            post
            join post_taboola_table ptt2 on ptt2.post_id = post.id
            join taboola t2 on t2.id = ptt2.taboola_id
        where
            post.domain_id = 2
            and post.id = 3
    ) as subtt on subtt.id = t.id
group by
    t.id