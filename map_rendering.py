import matplotlib.pyplot as plt
import numpy as np

import threat_calculator
import DMS_to_DD

#manually input iceberg coordinates 

convert = input("Are iceberg coordinates in DMS? (yes/no)")
if convert == "yes" or "yes":
    lat,lon = DMS_to_DD.convert(input("Separate the three terms by commas, dont include N/W, use a space to separate the longitude form latitude"))
else:
    lat,lon = [int(p) for p in input("separate the two decimals with a space").split(" ")]    
head = int(input("heading (as integer)"))
keel = int(input("keel depth (in meters)"))


#plot data, first entry is the iceberg
x = [lon,-48.74,-48.146,-48.4,-48.514]
y = [lat,46.75,46.7895,46.4,46.544]
labels = ["Iceberg", "Hibernia", "Sea Rose", "Terra Nova", "Hebron"]

# Blue is the iceberg
platform_colors = ["BLUE"]
subsea_colors = ["BLUE"]


# hardcoded platforms
hibernia_dict = {"name" : "Hibernia" ,"lat" : 46.75, "lon" : -48.74, "depth_m" : -78}
searose_dict = {"name" : "Sea Rose" ,"lat" : 46.7895, "lon" : -48.146, "depth_m" : -107}
terranova_dict = {"name" : "Terra Nova" ,"lat" : 46.4, "lon" : -48.4, "depth_m" : -91}
hebron_dict = {"name" : "Hebron" ,"lat" : 46.544, "lon" : -48.518, "depth_m" : -93}

#determining threat level
threats = threat_calculator.evaluate(lat,lon, head, keel, [hibernia_dict,searose_dict,terranova_dict,hebron_dict])

#colors of each
for platform_data in threats:
    platform_colors.append(platform_data['surface'])
    subsea_colors.append(platform_data['subsea'])


#Determining sample end points based on heading
theta = np.deg2rad(90-head)
end_x = lon + 100*np.cos(theta)
end_y = lat + 100*np.sin(theta)


# plot
fig, ax = plt.subplots(ncols = 1,nrows = 2, figsize = (2,5))

for i in range(2):
    # Plot the heading line from the iceberg
    ax[i].plot([lon, end_x], [lat, end_y], color='black', linestyle='-', label='Heading')

    ax[i].set(xlim = (-49.5,-45), ylim = (45.5,49.5))

    ax[i].set_xlabel("Longitude")
    ax[i].set_ylabel("Latitude")

    ax[i].grid(True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    ax[i].tick_params(top=True, right=True, labelbottom=True, labelleft=True)
    
    # Annotate the names of the platforms next to their dots
    for j, txt in enumerate(labels):
        ax[i].annotate(
            txt, 
            (x[j], y[j]), 
            textcoords="offset points",
            xytext=(6, 6),
            ha='left', 
            va='bottom',
            fontsize=9,
            weight='bold' if txt == "Iceberg" else 'normal'
        )

#Adding the colored points
ax[0].set(title = "Threat levels for platforms")
ax[1].set(title = "Threat levels for Subsea Assets below platforms")
ax[0].scatter(x, y, c=platform_colors)
ax[1].scatter(x, y, c=subsea_colors)

plt.tight_layout()
plt.show()



