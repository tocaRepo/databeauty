import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import matplotlib.offsetbox as offsetbox
import matplotlib.patheffects as path_effects  # Import path_effects
# Load the GDP per capita CSV file with error handling
try:
    data = pd.read_csv('gdp.csv', delimiter=',',
                       quotechar='"', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error reading the CSV file: {e}")
    exit()

# List of countries to focus on
countries_of_interest = ['Germany', 'Italy', 'United Kingdom', 'France',
                         'Japan', 'Spain', 'Australia', 'Canada', 'China', 'United States']

# Define a custom color map for each country
color_map = {
    'Germany': 'orange',
    'Italy': 'green',
    'United Kingdom': 'red',
    'France': 'purple',
    'Japan': 'white',
    'Spain': 'yellow',
    'Australia': '#00BFFF',  # Light Blue
    'Canada': 'cyan',
    'China': 'grey',
    'United States': 'blue'
}

# Path to flag images (ensure the path and file names match the country names)
flag_images = {
    'Germany': 'flags/germany.png',
    'Italy': 'flags/italy.png',
    'United Kingdom': 'flags/uk.png',
    'France': 'flags/france.png',
    'Japan': 'flags/japan.png',
    'Spain': 'flags/spain.png',
    'Australia': 'flags/australia.png',
    'Canada': 'flags/canada.png',
    'China': 'flags/china.png',
    'United States': 'flags/usa.png'
}

# Filter the data for the selected countries
filtered_data = data[data['Country Name'].isin(countries_of_interest)]

# Transform the data into a long format for easier plotting
df_long = filtered_data.melt(
    id_vars=["Country Name"], var_name="Year", value_name="GDP (current US$)")

# Filter out rows where 'Year' is not numeric
df_long = df_long[pd.to_numeric(df_long['Year'], errors='coerce').notna()]

# Convert 'Year' column to integer
df_long['Year'] = df_long['Year'].astype(int)

# Initialize the plot
fig, ax = plt.subplots(figsize=(9, 16))  # Full HD aspect ratio

# Set background color
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Function to add flags to the chart


def add_flag(ax, country, xpos, ypos):
    # Load the flag image
    flag_img = Image.open(flag_images[country])

    # Resize the image
    flag_img = flag_img.resize((50, 30))

    # Add image to plot as annotation box
    imagebox = offsetbox.OffsetImage(flag_img, zoom=0.8)
    ab = offsetbox.AnnotationBbox(
        imagebox, (xpos, ypos), frameon=False, box_alignment=(0, 0.5))
    ax.add_artist(ab)


def update(year):
    ax.clear()  # Clear the plot to redraw for each frame
    # Ensure the background remains black in each frame
    ax.set_facecolor('black')

    # Filter the data for the current year and sort by GDP
    df_year = df_long[df_long['Year'] == year].sort_values(
        by="GDP (current US$)", ascending=True)

    # Set the bar height to approximately match the flag size (adjust as needed)
    bar_height = 0.8  # Adjust this value as needed

    # Plot horizontal bars with the color map applied
    bars = ax.barh(df_year['Country Name'], df_year['GDP (current US$)'],
                   color=df_year['Country Name'].map(color_map), height=bar_height)

    # Add the title and labels
    ax.set_title(f'GDP in {year} (Billions)', fontsize=16, color='white')

    # Remove x-axis ticks and labels
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Adjust x-axis limits for better visibility
    max_gdp = df_long[df_long['Year'] == year]['GDP (current US$)'].max()
    ax.set_xlim(0, max_gdp * 1.1)

    # Annotate each bar with the GDP value in billions and add flags
    for bar, country in zip(bars, df_year['Country Name']):
        width = bar.get_width()
        ypos = bar.get_y() + bar.get_height() / 2

        # Add the flag just after the end of the bar
        add_flag(ax, country, width + 0.001 * max_gdp, ypos)

        # Add the GDP value
        text = ax.text(width - 0.077 * max_gdp, ypos,
                       f'{width / 1e9:.0f}$', va='center', fontsize=10, color='white')
        text.set_path_effects(
            [path_effects.withStroke(linewidth=1, foreground='black')])

    # Ensure y-axis labels are set
    ax.set_yticks(df_year['Country Name'])
    ax.set_yticklabels(df_year['Country Name'], color='white')


# Create the animation
years = sorted(df_long['Year'].unique())
repeat_frames = 8
extended_years = years + [years[-1]] * repeat_frames
ani = FuncAnimation(fig, update, frames=extended_years,
                    repeat=False, interval=100)
# Save the animation as a video
# You can adjust fps and filename
ani.save('gdp_animation.mp4', writer='ffmpeg', fps=1.8)

# Show the animation
plt.show()
