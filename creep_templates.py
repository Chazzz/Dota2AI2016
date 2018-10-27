# 1080p templates for dire and radiant creeps

from get_image import load_image, show_image

base_creep_img = load_image("creeps1080p.png")
base_creep_img_2 = load_image("creeps_1080p_dire.png")
# print base_creep_img[544:548,1299:1303,:]
# print base_creep_img[1299:1302,544:546,:]

# print base_creep_img[348,951,:]
# show_image(base_creep_img[295:296,839+1:839+79,:])
# show_image(base_creep_img[295-1:296+1,839:839+80,:])




# show_image(base_creep_img)

# cropimg = base_creep_img[250:450, 600:900,:]
# cropimg_2 = base_creep_img[300:600, 800:1400,:]
# show_image(cropimg_2)
rad_template = base_creep_img[360:366,649:650,:]
dir_template = base_creep_img_2[102:108,1131:1132,:]
# print dir_template.shape
# show_image(dir_template)
