# Realtor.com Agents by Zip Code Scraper

> A focused Realtor.com agent scraper that finds and enriches real estate agent profiles by zip code. It pulls names, contact details, sales performance, coverage areas, and more, helping you build high-quality, local agent lead lists. Use it to power outreach, analytics, and market research with structured, ready-to-use data.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Realtor.com Agents by Zip Code</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

Realtor.com Agents by Zip Code Scraper is a specialized tool for collecting agent data tied to specific postal codes. You provide one or more zip codes, and the scraper searches Realtor.com for agents servicing those areas, then exports their profiles in a structured format.

This project is ideal for real estate marketers, brokerages, SaaS tools, and analysts who need accurate, up-to-date agent information for prospecting, lead scoring, or territory analysis. By automating manual profile lookups, it saves hours of repetitive work and ensures you always work with consistent, machine-readable data.

### Targeted Realtor Agent Intelligence

- Focuses on agents that actively service the zip codes you specify.
- Captures both performance metrics (listings, sold count, reviews) and contact channels.
- Supports optional cookie and User-Agent overrides to improve reliability on protected pages.
- Produces clean JSON/CSV output for direct use in CRMs, dashboards, and analytics tools.
- Designed for users of all technical levels, from non-technical marketers to data engineers.

## Features

| Feature | Description |
|----------|-------------|
| Zip code–based agent discovery | Scrapes agents who explicitly service the zip codes you provide, ensuring the data aligns with your target territories. |
| Rich contact enrichment | Collects emails, office phone, and mobile phones where available, making the data ready for compliant outreach workflows. |
| Performance & activity metrics | Extracts listing counts, sold counts, and review counts to help you prioritize top-performing agents. |
| Coverage & territory mapping | Captures areas and zip codes serviced by each agent so you can analyze coverage and identify gaps. |
| Company & branding details | Pulls office/company name and website fields for better organization and segmentation. |
| Optional cookie & User-Agent support | Allows you to provide your KP_UIDz-ssn cookie and User-Agent string to reduce the chance of being blocked and improve result consistency. |
| Trial-friendly output limit | Trial usage can be limited to a small number of records (e.g., 5) for quick testing before scaling up. |
| Export-ready structured data | Outputs structured records suitable for importing into CRM systems, spreadsheets, BI tools, or custom applications. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| Agent name | Full name of the real estate agent, including any role or team designation. |
| Website | Link to the agent’s personal page or Realtor.com profile. |
| Email | Agent’s email address, when publicly available. Use only in compliance with applicable communication and anti-spam laws. |
| Listing count | Number of active listings the agent currently has on Realtor.com. |
| Sold count | Number of properties the agent has sold, indicating experience and activity level. |
| Office Phone | Office or brokerage phone number, if provided. May be null when not available. |
| Mobile Phones | One or more mobile phone numbers listed for the agent. May be empty when not available. |
| Areas serviced | Human-readable list of areas or neighborhoods the agent serves. |
| Zip codes serviced | Comma-separated list of zip codes where the agent provides services. |
| Office / Company name | Name of the agent’s office, brokerage, or company. May be empty for independent agents. |
| Company Website | Website of the office or company, if available. May be null or empty when not provided. |
| Review count | Total number of reviews the agent has on Realtor.com, useful for gauging reputation. |
| Agent Photo | URL of the agent’s photo or avatar, when available. |

---

## Example Output

Example:

    [
      {
        "Agent name": "David Solomon, Agent, agent",
        "Website": "https://www.realtor.com/realestateagents/David-Solomon_Brentwood_CA_748820_292674308",
        "Email": "David@realtordomain.com",
        "Listing count": 11,
        "Sold count": 48,
        "Office Phone": "(310) 270-xxxx",
        "Mobile Phones": "(310) 279-xxxx, (310) 633-xxxx",
        "Areas serviced": "Los Angeles, Beverly Hills, Malibu, Santa Monica, West Hollywood, Venice, Marina del Rey, Pacific Palisades, Brentwood, Bel Air, ",
        "Zip codes serviced": "90049, 90068, 90210, 90265, 90402, 90401, 90403, 90069, 90291, 90292, 90272",
        "Office / Company name": "Brentwood",
        "Company Website": null,
        "Review count": 0,
        "Agent Photo": "https://ap.rdcpix.com/162885285/191adfd4aedfdf87891cf243b5bce3e3a-e0s.jpg"
      }
    ]

---

## Directory Structure Tree

    realtor-com-agents-by-zip-code-scraper/
    ├── src/
    │   ├── main.py
    │   ├── config.py
    │   ├── realtor_client.py
    │   ├── agent_extractor.py
    │   ├── pagination_manager.py
    │   ├── parsers/
    │   │   ├── html_parser.py
    │   │   └── agent_normalizer.py
    │   ├── storage/
    │   │   ├── csv_exporter.py
    │   │   └── json_exporter.py
    │   └── utils/
    │       ├── logger.py
    │       └── rate_limiter.py
    ├── config/
    │   ├── settings.example.yaml
    │   └── user_agents.sample.txt
    ├── data/
    │   ├── input_zip_codes.sample.json
    │   └── sample_output.agents.json
    ├── tests/
    │   ├── test_agent_extractor.py
    │   ├── test_realtor_client.py
    │   └── test_parsers.py
    ├── scripts/
    │   └── run_scraper_from_cli.sh
    ├── .env.example
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Real estate brokerages** use it to **discover and segment local agents by performance and territory**, so they can **identify top producers for recruiting or partnerships**.
- **Marketing agencies** use it to **build targeted Realtor outreach lists with emails and phone numbers**, so they can **run compliant, high-conversion campaigns for services and tools**.
- **Proptech and SaaS platforms** use it to **enrich CRM or application data with agent performance metrics and coverage areas**, so they can **improve lead routing, recommendations, and analytics**.
- **Market researchers and analysts** use it to **map agent density and activity across zip codes**, so they can **understand competitive landscapes and regional dynamics**.
- **Investors and wholesalers** use it to **quickly find experienced agents in specific investment markets**, so they can **build local teams and accelerate deal flow**.

---

## FAQs

**Q: Do I have to provide my KP_UIDz-ssn cookie and User-Agent string?**
A: No, these fields are optional. The scraper can run with default values, but providing your own KP_UIDz-ssn cookie and User-Agent often improves reliability and reduces the chance of being blocked, especially when scraping many agents or running frequent sessions.

**Q: Can I scrape multiple zip codes at once?**
A: Yes. You can pass a list of zip codes in the input file or configuration. The scraper will iterate through them, collecting agents for each zip code and combining the results into a single dataset.

**Q: Is this scraper legal to use?**
A: The tool collects publicly available information for informational and analytical purposes. It is your responsibility to ensure that your usage complies with relevant laws, website terms, and regulations, particularly regarding email outreach, telemarketing, and privacy. Always respect do-not-contact policies and anti-spam rules.

**Q: Are there limits for trial users or small tests?**
A: You can configure the scraper to limit the number of records returned for evaluation runs (for example, to 5 agents). This helps you verify that the configuration, fields, and output format meet your needs before running larger jobs.

---

## Performance Benchmarks and Results

- **Primary Metric – Scraping Throughput:** On a stable connection and with reasonable rate limits, the scraper can typically process dozens of agents per minute per zip code, depending on protection mechanisms and delays you configure.
- **Reliability Metric – Success Rate:** With valid cookie and User-Agent values, successful agent profile retrieval can exceed 90% for reachable profiles, with automatic retries on transient failures.
- **Efficiency Metric – Resource Usage:** Designed to run on modest hardware, it can operate comfortably on a small cloud instance or local machine while respecting polite delays and rate limits.
- **Quality Metric – Data Completeness:** For most agents, the scraper returns a high-completeness profile including name, profile URL, performance metrics, and service areas, with optional contact fields populated whenever they are publicly exposed on the page.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
