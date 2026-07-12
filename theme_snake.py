import re

file_path = "d:\\Pranav-496\\github-user-contribution.svg"
with open(file_path, "r", encoding="utf-8") as f:
    svg = f.read()

# Replace variables
# We want blood red and black theme:
# --cb (border): rgba(255,0,0,0.15)
# --ce (empty): #0D1117 -> #1E1E2E or #120000
# --c0 (lowest): -> #1A0000
# --c1 (low): -> #4D0000
# --c2 (med): -> #8B0000
# --c3 (high): -> #CC0000
# --c4 (highest): -> #FF0000
# --cs (snake): url(#snake-grad)

css_vars = "--cb:rgba(255,0,0,0.15);--cs:url(#snake-grad);--ce:#120505;--c0:#120505;--c1:#4D0000;--c2:#8B0000;--c3:#CC0000;--c4:#FF0000"
svg = re.sub(r':root\{[^\}]+\}', f":root{{{css_vars}}}", svg)

# Inject defs right after <svg ...>
defs = """<defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0D0000"/>
        <stop offset="100%" stop-color="#050000"/>
    </linearGradient>
    <linearGradient id="snake-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FF1A1A"/>
        <stop offset="100%" stop-color="#8B0000"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur1" />
        <feGaussianBlur stdDeviation="8" result="blur2" />
        <feMerge>
            <feMergeNode in="blur2"/>
            <feMergeNode in="blur1"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>"""

# If there's already a bg-grad or glow, we should remove them before re-injecting,
# but the script is just running on the *already modified* SVG or the original?
# The user ran it on the original before. Since we already modified it, we might have multiple defs.
# Let's restore the original from github first, then apply. 
# Wait, do I have the original? No. I'll just strip out existing <defs> and background rect to be safe.

svg = re.sub(r'<defs>.*?</defs>', '', svg, flags=re.DOTALL)
svg = re.sub(r'<rect width="100%" height="100%" fill="url\(#bg-grad\)".*?/>', '', svg)

svg = re.sub(r'(<svg[^>]*>)', r'\1' + defs + '<rect width="100%" height="100%" fill="url(#bg-grad)" x="-5%" y="-5%" rx="16"/>', svg, count=1)

# Modify `.s` (the snake) to have a glow
if '.s{filter:url(#glow);' not in svg:
    svg = svg.replace('.s{', '.s{filter:url(#glow);')
if '.c{rx:4;ry:4;' not in svg:
    svg = svg.replace('.c{', '.c{rx:4;ry:4;')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(svg)
print("Themed successfully to Blood Red and Black.")
