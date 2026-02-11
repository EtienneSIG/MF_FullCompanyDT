# Example Questions for Fabric Data Agent

## 📋 Overview

Collection of 50+ natural language questions organized by complexity and business domain for testing the Fabric Data Agent.

**Usage:**
- Test agent configuration
- Train business users
- Validate cross-domain analysis capabilities

---

## ✅ Level 1: Simple Single-Table Queries

### Sales Domain

1. "What was our total revenue last month?"
2. "How many orders did we have yesterday?"
3. "What's the average order value?"
4. "Show me top 10 products by revenue"
5. "What's our gross margin percentage?"

### Customer Domain

6. "How many customers do we have?"
7. "How many active customers are there?"
8. "Which customer segment has the most customers?"
9. "List top 5 customers by revenue"
10. "What's the average customer lifetime value?"

### Support Domain

11. "How many support tickets are open?"
12. "What's our average CSAT score?"
13. "How many tickets were resolved yesterday?"
14. "What's the average resolution time?"
15. "What percentage of tickets are resolved on first contact?"

---

## 🔄 Level 2: Time-Based Comparisons

### Year-over-Year

16. "Compare revenue this year vs last year"
17. "What's our YoY growth rate?"
18. "How has CSAT changed year-over-year?"
19. "Compare attrition rate this year vs last year"

### Month-over-Month

20. "What's the month-over-month revenue change?"
21. "Did support tickets increase or decrease this month?"
22. "Show me monthly revenue trend for the last 12 months"
23. "How has inventory turns changed month-over-month?"

### Quarter Comparisons

24. "What was revenue in Q4 compared to Q3?"
25. "Show me quarterly revenue trend"
26. "Which quarter had the highest customer growth?"

---

## 🔗 Level 3: Cross-Domain Analysis

### Revenue & Support

27. "Do customers with low CSAT scores have declining revenue?"
28. "Which products have the most support tickets and how does it impact sales?"
29. "Show correlation between CSAT and customer retention"
30. "Are high-value customers getting better support (faster resolution times)?"

### Sales & Inventory

31. "Are stockouts impacting revenue?"
32. "Which products are out of stock and what's the lost revenue opportunity?"
33. "Show products with low inventory and high demand"
34. "How does inventory turns correlate with sales volume?"

### HR & Operations

35. "Does employee attrition correlate with IT incidents?"
36. "Which departments have high attrition and how does it impact SLAs?"
37. "Show relationship between manager attrition and team performance"
38. "Do departments with high attrition have longer support resolution times?"

### Finance & Operations

39. "Compare budget vs actuals for departments with high attrition"
40. "Which cost centers are over budget and by how much?"
41. "Show variance between budgeted and actual cloud spend"

---

## 🧠 Level 4: Complex Multi-Step Reasoning

### Root Cause Analysis

42. **"Why did revenue drop in EMEA last month and what can we do about it?"**
   - Expected: Analyze sales, inventory, support, and supplier data
   - Link stockouts, customer complaints, and delivery delays

43. **"Explain the revenue decline in Q4 - was it demand, supply chain, or quality issues?"**
   - Expected: Cross-reference sales, inventory, defects, and support tickets

44. **"What's causing high attrition in the Engineering department and what's the business impact?"**
   - Expected: Link HR data with project delays, incident resolution times

### Trend Analysis & Prediction

45. **"Based on current trends, will we hit our annual revenue target?"**
   - Expected: Analyze YTD revenue, growth rates, seasonality

46. **"Which products are declining in sales and should we discontinue them?"**
   - Expected: Sales trends, inventory costs, support burden

47. **"Identify customers at risk of churning based on support and purchase patterns"**
   - Expected: CSAT trends, purchase frequency, ticket volume

### Impact Analysis

48. **"What's the financial impact of IT downtime incidents on revenue?"**
   - Expected: Correlate incident times with sales data, calculate lost revenue

49. **"How much revenue did we lose due to stockouts last quarter?"**
   - Expected: Identify stockout periods, compare to historical demand

50. **"What's the ROI of reducing support resolution time by 20%?"**
   - Expected: Calculate CSAT improvement, retention impact, revenue effect

---

## 🎯 Level 5: Strategic Business Questions

### Executive Dashboard Questions

51. **"Give me an executive summary of business performance this quarter"**
   - Expected: Revenue, margin, customer growth, CSAT, attrition, key issues

52. **"What are the top 3 risks to hitting our Q4 targets?"**
   - Expected: Identify inventory issues, quality problems, resource constraints

53. **"Where should we invest to maximize customer satisfaction and retention?"**
   - Expected: Analyze support performance, product quality, delivery times

### Comparative Analysis

54. **"Compare EMEA vs Americas performance across all KPIs"**
   - Expected: Revenue, margin, CSAT, delivery times, returns by region

55. **"Which customer segment is most profitable and why?"**
   - Expected: Revenue, margin, support costs, retention by segment

56. **"What's our best-performing product category and what makes it successful?"**
   - Expected: Revenue, margin, quality, support tickets, returns

### Anomaly Detection

57. **"Are there any unusual patterns in sales, support, or operations data?"**
   - Expected: Identify spikes, drops, outliers across domains

58. **"Which customers or products show concerning trends?"**
   - Expected: Declining revenue, increasing complaints, quality issues

---

## 💡 Testing Guidelines

### Validation Checklist

For each question:

- [ ] Agent provides a specific numerical answer (not vague)
- [ ] Agent cites source tables/measures used
- [ ] Response includes context (comparisons, trends)
- [ ] Recommendations are actionable (when appropriate)
- [ ] No hallucinated data (verify against semantic model)
- [ ] Response time < 10 seconds

### Success Criteria

**Level 1-2:** 95%+ accuracy (straightforward queries)  
**Level 3:** 85%+ accuracy (cross-domain joins)  
**Level 4:** 75%+ accuracy (multi-step reasoning)  
**Level 5:** 60%+ accuracy (strategic insights)

### Common Failure Modes

1. **Ambiguous time references:** "last month" when run mid-month
   - Fix: Add time reference clarification in instructions

2. **Wrong table selection:** Uses opportunities instead of sales
   - Fix: Add usage guidelines per table in instructions

3. **Missing context:** Gives number without comparison
   - Fix: Update response format guidelines

4. **Incomplete correlations:** Only checks one domain
   - Fix: Add cross-domain pattern examples

---

## 🔧 Customization

### Add Your Questions

Format:
```
## Your Category

1. "Your question?"
   - Expected: What the agent should include in response
   - Complexity: Level 1-5
```

### Map to Business Scenarios

Link questions to:
- Executive reviews (monthly/quarterly)
- Operational stand-ups (daily/weekly)
- Incident investigations (ad-hoc)
- Strategic planning (annual)

---

## 📊 Usage Tracking

Track which questions are:
- ✅ Most frequently asked → Add as verified answers
- ⚠️ Frequently failing → Improve metadata/instructions
- 🔥 Generating insights → Share with stakeholders

---

**Total Questions:** 58  
**Coverage:** 10+ domains  
**Complexity Levels:** 5  
**Ready for:** Agent testing and user training
