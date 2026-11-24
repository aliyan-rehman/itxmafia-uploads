# Swirlverse content formats and the viral-research gate

The channel is no longer "what if" only. Any **curiosity video** that fits Swirlverse is allowed. Every video must be all three:
- science or psychology based
- explained by Nova and Kiko
- fun

Every run must research the topic and score it **before** writing anything.

## 1. Formats (pick the one that fits the topic best)
| Format | Title pattern | Kit shots | Example |
|---|---|---|---|
| **WHAT IF** (parallel world) | What If <thing> Was <CAPS twist>? | hook → arrive → inserts → end | What If We Didn't Need SLEEP? |
| **WHY** (everyday mystery) | Why <surprising everyday fact>? / Why You Should NEVER <x> | cold_open → kcu/ncu → stat/custom → verdict or end | Why You Shouldn't Decide When ANGRY |
| **IS IT TRUE?** (myth or fact) | Is <common belief> TRUE? / <belief>? MYTH! | cold_open → test/custom → verdict(MYTH!/TRUE!/IT DEPENDS) → end | Do Big and Small Tyres Travel the SAME 100 km? |
| **VS** (showdown) | <A> vs <B>: Which Wins? | cold_open → versus → compare/stat → verdict → end | Cold Shower vs Hot Shower |
| **MIND HACK** (psychology) | Your Brain Does THIS When… | cold_open → custom brain/board → stat → end | Why Songs Get STUCK in Your Head |
| **IMAGINE** (belief or legend, told respectfully) | What If <belief> Was REAL? | hook (portal) → arrive → story → science angle → end | What If We Really Had 7 Lives? |

- **Portal:** WHAT IF and IMAGINE use the portal ("In our world… but in this parallel world…"). The other formats may use it as a twist ("let's test it in a parallel world"), but don't have to.
- **Endings:** always end with a 2-option question or poll, and "A new parallel world, every day." (or "New mystery every day.").
- **Shorts:** 25–45 s, with the hook in the first 2 s. Show the question on screen immediately with `K.cold_open(question=…)`.

## 2. Research gate (must pass, write the result into the episode docstring)
1. **Is it true?** Check every claim with WebSearch, with at least 2 independent reliable sources: .gov or .edu, encyclopedias, peer-reviewed papers, major science outlets. Note the numbers exactly and round honestly. If the honest answer is "it depends", say so: it's a great verdict.
2. **Do people actually wonder about it?** Look for evidence of real curiosity:
   - "People also ask" style questions in search results
   - Reddit, Quora or forum threads
   - news from the last 12 months, trending events, seasonal hooks (exams, winter, festivals, World Cup…)
   - viral claims doing the rounds
3. **Is our angle fresh?** Search `"<topic>" youtube`, `what if <topic>`, `why <topic>`.
   - If big channels already made the same angle, find a twist (a parallel-world test, a surprising number, a versus, a local angle) or pick another topic.
   - Never copy another channel's script, title, thumbnail or characters.
4. **Score it 1–5** on each of these, and only make it if the **total is ≥ 19/25** and no score is 1:
   - Curiosity gap: would someone stop scrolling to know the answer?
   - Relatable: everyday life or something everyone has wondered
   - Visual: can we show it in one clear, funny image?
   - Fact certainty: solid sources
   - Freshness: our angle isn't already everywhere
5. Log the format, the score and 2–3 source names in the STRATEGY.md experiment row.

## 3. Title + thumbnail = one curiosity gap
- **Title:** ask the question or tease the surprise. Don't give the answer away.
  - Use 1 CAPS word and, where possible, a number: "Why You Should NEVER Decide When ANGRY", "Is 100 km the SAME on Every Tyre?"
  - Keep it under 60 characters and honest: the video must answer it.
- **Thumbnail:** don't repeat the title. Add to it, using thumbkit's burst, big_text, arrow and emoji_burst:
  - 2–4 huge words
  - 1 BIG character with an extreme face
  - 1 hero object
  - an arrow, a "?!" sticker or a verdict stamp
  - It must show something that really happens in the video. Never fake a result.
- Shorts: keep the text in the top 45%. Long videos: put the text on the left or right third, with the face on the other side.

## 4. Sensitive topics (religion, culture, health, money)
- **Beliefs** (rebirth/7 janams, astrology, ghosts, luck):
  - Allowed only as respectful **IMAGINE** stories.
  - Say clearly that it is a belief held by many people ("In Hindu belief…"). Never mock it, and never claim a religion is true or false.
  - The science part talks only about what science can measure (memory, probability, biology).
  - No gods or holy figures as characters. No sacred symbols used as jokes.
- **Health:** general, well-sourced facts only. Never give medical advice or dosages. Add "talk to a doctor" if it's relevant.
- No politics, no tragedies or disasters for views, no fear-bait, nothing a child shouldn't see.

## 5. Idea bank (examples from the owner; research before using, then add new ones)
| Format | Idea |
|---|---|
| IMAGINE | What if we really had 7 janams (rebirth)? (respectfully, see section 4) |
| IS IT TRUE / VS | Do different-size tyres travel the same 100 km? (odometer, revolutions per km, why the speedometer reads wrong with the wrong tyre size) |
| WHY / MIND HACK | Why you shouldn't make decisions when very happy or very angry |
| WHAT IF | What if humans never needed sleep? |

More directions: why we yawn when others yawn, why time feels faster as you get older, is 5-second rule true, why onions make you cry, cold vs hot water freezing faster (Mpemba), why cats always land on feet, what if the internet stopped for a day, what if we could photosynthesise, why we can't tickle ourselves, is a dog year really 7 human years.
