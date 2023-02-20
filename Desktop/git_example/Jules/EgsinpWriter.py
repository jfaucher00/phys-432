path_template = "C:/Users/jules/Desktop/template.egsinp"
path_output = "C:/Users/jules/Desktop/output.egsinp"

thickness = 4.5

with open(path_template, "r") as template_file:
    template = template_file.read()

new_input = template.format(envelope_thickness = thickness + 0.5, 
                            envelope_z = 52.7565 - 0.5*(thickness + 0.5),
                            density_path = "test/path", 
                            ramp_path = "another/test",
                            paddle_z = 52.476 - thickness, 
                            kvp = 28, 
                            medium = "PMMA_l")

with open(path_output, "w") as new_file:
    new_file.write(new_input)