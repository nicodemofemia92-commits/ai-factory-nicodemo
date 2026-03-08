
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")

prompt = """
You are a B2B lead generation expert.

Create a lead discovery list for selling niche market analysis reports.

Return:

1. 20 companies or company types to target
2. 20 Google search queries to find them
3. 10 LinkedIn search queries
4. 10 directories or websites where they can be found
5. 10 example company names
6. 5 outreach messages

Focus on:
- marketing agencies
- SEO consultants
- founders
- freelancers
- real estate agencies
- consultants

Format clearly.
"""

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    output = response.text

except Exception as e:

    output = f"""
[DEMO LEAD MACHINE]

TARGET COMPANIES
marketing agencies
seo consultants
growth consultants
branding studios
real estate agencies
web design agencies
local consultants
startup founders
lead generation agencies
digital agencies

SEARCH QUERIES
marketing agency Milan
seo consultant Italy
startup founder LinkedIn
branding studio Milan
real estate agency Milan
digital agency Rome
web design agency Italy
consultant business strategy Italy
growth consultant London
marketing freelancer Italy

LINKEDIN SEARCH
marketing agency owner
seo consultant
startup founder
freelance marketer
agency owner
growth consultant
branding consultant
real estate agency owner
web design agency owner
consultant strategy

DIRECTORIES
clutch.co
sortlist.com
goodfirms.co
designrush.com
linkedin.com
google maps
yelp
agencyspotter
angel.co
producthunt

COMPANY EXAMPLES
GrowthLab
Milan Marketing Co
Digital Boost Agency
Prime SEO Studio
Realty Milano
BrandForge
Growth Rocket
LeadGen Labs
Agency Milano
Scale Marketing

OUTREACH
Hey,

I built a tool that generates a strategic market brief for any niche.

It shows:
competitors
positioning
monetization angles

If you want I can generate one for your market.

"""

print(output)

folder = os.path.expanduser("~/ai_factory/leads")
os.makedirs(folder, exist_ok=True)

path = os.path.join(folder, f"lead_machine_{today}.txt")

with open(path,"w") as f:
    f.write(output)

print("\nSaved to:",path)
