// CodaiPro website — reveal-on-scroll, live star count, real poll.
// The poll stores votes as GitHub issues in the public repository and counts
// them through the public GitHub API. No accounts, no cookies, no backend.
// Everything degrades gracefully: without JS or when the API is unreachable,
// the vote links still work and the page still reads fine.

(function () {
    "use strict";

    var REPO = "Luckyyaduvanshiofficial/Codai";
    var CACHE_MS = 10 * 60 * 1000; // be kind to the unauthenticated rate limit

    document.documentElement.classList.add("js");

    // localStorage can throw outright when cookies/site data are blocked
    var LS = (function () {
        try {
            var t = window.localStorage;
            t.setItem("__codaipro_test", "1");
            t.removeItem("__codaipro_test");
            return t;
        } catch (e) {
            var mem = {};
            return {
                getItem: function (k) { return Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : null; },
                setItem: function (k, v) { mem[k] = String(v); },
                removeItem: function (k) { delete mem[k]; }
            };
        }
    })();

    function cacheGet(key) {
        try {
            var raw = LS.getItem(key);
            if (!raw) return null;
            var parsed = JSON.parse(raw);
            return parsed;
        } catch (e) {
            return null;
        }
    }

    function cacheSet(key, value) {
        try {
            LS.setItem(key, JSON.stringify(value));
        } catch (e) {
            /* private mode or quota — non-fatal */
        }
    }

    /* ----------------------------------------------------------------------
       Footer year
       ---------------------------------------------------------------------- */

    var year = document.getElementById("year");
    if (year) year.textContent = String(new Date().getFullYear());

    /* ----------------------------------------------------------------------
       Live star count in the hero chip
       ---------------------------------------------------------------------- */

    var chipText = document.getElementById("gh-chip-text");

    if (chipText) {
        var starsCache = cacheGet("codaipro-stars");

        var paintStars = function (n, forks) {
            chipText.innerHTML =
                "<strong>★ " + n + "</strong> stars" +
                (forks != null ? " · " + forks + " forks" : "") +
                " on GitHub — add yours";
        };

        if (starsCache && Date.now() - starsCache.t < CACHE_MS) {
            paintStars(starsCache.stars, starsCache.forks);
        } else {
            fetch("https://api.github.com/repos/" + REPO)
                .then(function (r) { return r.ok ? r.json() : null; })
                .then(function (d) {
                    if (!d || typeof d.stargazers_count !== "number") return;
                    cacheSet("codaipro-stars", {
                        t: Date.now(),
                        stars: d.stargazers_count,
                        forks: d.forks_count
                    });
                    paintStars(d.stargazers_count, d.forks_count);
                })
                .catch(function () { /* keep the static fallback text */ });
        }
    }

    /* ----------------------------------------------------------------------
       Poll — votes are "[Poll] <Option>" issues in REPO
       ---------------------------------------------------------------------- */

    var POLL_OPTIONS = [
        { label: "Phi-3.5-mini" },
        { label: "Qwen2.5-Coder-3B" },
        { label: "Qwen2.5-Coder-7B" },
        { label: "Still deciding" }
    ];
    var POLL_MARKER = "[Poll]";
    var VOTE_KEY = "codaipro-vote";       // this browser's choice
    var RESULTS_KEY = "codaipro-poll-results";

    var resultsBox = document.getElementById("poll-results");
    var totalEl = document.getElementById("poll-total");
    var rowsEl = document.getElementById("poll-rows");
    var optionLinks = document.querySelectorAll(".poll-option");

    var myVote = null;
    try { myVote = LS.getItem(VOTE_KEY); } catch (e) { /* ignore */ }

    // Mark the remembered choice
    optionLinks.forEach(function (link) {
        if (link.getAttribute("data-poll-label") === myVote) {
            link.classList.add("is-voted");
        }
        link.addEventListener("click", function () {
            try { LS.setItem(VOTE_KEY, link.getAttribute("data-poll-label")); } catch (e) { /* ignore */ }
        });
    });

    if (!resultsBox || !totalEl || !rowsEl) return;

    function countFromTitle(title) {
        var t = (title || "").trim();
        if (t.indexOf(POLL_MARKER) !== 0) return null;
        var label = t.slice(POLL_MARKER.length).trim();
        for (var i = 0; i < POLL_OPTIONS.length; i++) {
            if (POLL_OPTIONS[i].label === label) return POLL_OPTIONS[i].label;
        }
        return null;
    }

    function renderResults(counts, total, cached) {
        resultsBox.hidden = false;
        totalEl.textContent =
            total === 0
                ? "No votes yet — be the first." + (cached ? " (showing cached tally)" : "")
                : total + (total === 1 ? " vote" : " votes") + " counted" + (cached ? " (cached)" : "");

        rowsEl.innerHTML = "";
        POLL_OPTIONS.forEach(function (opt) {
            var count = counts[opt.label] || 0;
            var pct = total > 0 ? Math.round((count / total) * 100) : 0;

            var li = document.createElement("li");
            li.className = "poll-row";

            var label = document.createElement("span");
            label.className = "poll-label";
            label.textContent = opt.label;
            if (opt.label === myVote) {
                var yours = document.createElement("span");
                yours.className = "yours";
                yours.textContent = " — your vote";
                label.appendChild(yours);
            }

            var countEl = document.createElement("span");
            countEl.className = "poll-count";
            countEl.textContent = String(count);

            var track = document.createElement("span");
            track.className = "poll-track";
            var fill = document.createElement("span");
            fill.className = "poll-fill";
            track.appendChild(fill);

            li.appendChild(label);
            li.appendChild(countEl);
            li.appendChild(track);
            rowsEl.appendChild(li);

            // animate in on the next frame
            requestAnimationFrame(function () {
                requestAnimationFrame(function () {
                    fill.style.width = (pct || (count > 0 ? 2 : 0)) + "%";
                });
            });
        });
    }

    function showUnavailable() {
        resultsBox.hidden = false;
        var cached = cacheGet(RESULTS_KEY);
        if (cached && cached.counts) {
            renderResults(cached.counts, cached.total, true);
            return;
        }
        resultsBox.innerHTML =
            '<p class="poll-unavailable">Live tally is unavailable right now ' +
            "(GitHub API rate limit or offline). Your vote button still works — " +
            'results will appear on your next visit.</p>';
    }

    var resultsCache = cacheGet(RESULTS_KEY);

    if (resultsCache && Date.now() - resultsCache.t < CACHE_MS) {
        renderResults(resultsCache.counts, resultsCache.total, true);
    } else {
        fetch("https://api.github.com/repos/" + REPO + "/issues?per_page=100&state=all&sort=created&direction=desc")
            .then(function (r) {
                if (!r.ok) throw new Error("github api " + r.status);
                return r.json();
            })
            .then(function (issues) {
                if (!Array.isArray(issues)) throw new Error("unexpected response");

                var counts = {};
                var total = 0;
                issues.forEach(function (issue) {
                    // issues list includes pull requests; they are not votes
                    if (issue.pull_request) return;
                    var label = countFromTitle(issue.title);
                    if (!label) return;
                    counts[label] = (counts[label] || 0) + 1;
                    total += 1;
                });

                cacheSet(RESULTS_KEY, { t: Date.now(), counts: counts, total: total });
                renderResults(counts, total, false);
            })
            .catch(showUnavailable);
    }

    /* ----------------------------------------------------------------------
       Reveal on scroll
       ---------------------------------------------------------------------- */

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var targets = document.querySelectorAll(
        ".hero-copy, .sheet, .section-head, .syllabus-list li, " +
        ".option, .models, .venues-list li, .letter"
    );

    if (reduced || !("IntersectionObserver" in window)) return;

    targets.forEach(function (el) { el.classList.add("reveal-init"); });

    var observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;

                var el = entry.target;
                // Stagger siblings that arrive together; human jitter, not metronome.
                var siblings = Array.prototype.filter.call(
                    el.parentNode.children,
                    function (c) { return c.classList.contains("reveal-init"); }
                );
                var index = siblings.indexOf(el);
                el.style.transitionDelay = (Math.max(index, 0) % 6) * 70 + "ms";

                el.classList.add("is-in");
                observer.unobserve(el);
            });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    targets.forEach(function (el) { observer.observe(el); });
})();
