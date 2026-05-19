# Patch Acceptance Rule

Formal criterion for accepting or rejecting a heuristic rule into the symbolic pipeline.

## The Rule

A verify condition (or any pipeline patch) is **accepted** if and only if ALL of:

1. **Support >= 10** on inner_dev (the rule fires on at least 10 inner-dev images)
2. **inner_dev net positive** (helped > hurt on the held-out 50/class inner dev split)
3. **No class collapse** (no single class loses more than 2 images on inner_dev)
4. **Not a fix-1 threshold** (the rule does not exist to correct a single image)
5. **Complexity bounded** (at most 2 conjunctive conditions, thresholds rounded to 2 significant digits)

## Measurement Protocol

1. **Propose** a new rule by observing patterns on inner_train (150/class)
2. **Score** the rule using `hlinet/eval/rule_credit.py` which measures:
   - support: how many images the rule fires on
   - helped/hurt: how many it corrects vs breaks
   - per-class damage: whether any single class is disproportionately harmed
   - transfer ratio: dev_net / train_net
3. **Accept or reject** based on the criteria above
4. **Report** val as a passive monitor (never use val to make acceptance decisions)
5. **Test** remains untouched until final reporting

## Why Inner_Dev Is Imperfect

The verify audit showed that inner_dev says verify is net-positive (+78 on 500 images)
while val says it's net-negative (-50 on 2000 images). This happens because:

- Inner_dev shares the same image distribution as inner_train (same source)
- Rules tuned on ANY subset of train will generalize within train better than to val
- The true distribution shift is train→val, not inner_train→inner_dev

**Mitigation**: Set high support threshold (>=10) and require STRONG net positive,
not marginal. Rules that pass with support=10 and net=+1 are likely noise.

## Future Improvements

- Use augmentation-based pseudo-val (flip, brightness, contrast transforms)
- Require rules to survive 3-fold cross-validation within train
- Weight acceptance by complexity: simpler rules get lower support thresholds
- Track rule lifetime: if a rule's val contribution turns negative after 3 sessions, remove it

## Complexity Score

| Factor | Cost |
|--------|:---:|
| Each threshold comparison | +1 |
| Each AND condition | +1 |
| Threshold with >3 significant digits | +1 |
| Feature not used elsewhere in pipeline | +2 |
| Pair not in pairwise reranking | +1 |

Maximum allowed complexity: 5 points.

## Current Status

As of Session 22b, the acceptance rule retroactively evaluates existing rules:
- **38 unique pair blocks** across 4 verify stages
- Rule-level credit assignment running (ablation-based)
- Jellyfish and banana pair blocks are the only ones empirically passing on val
