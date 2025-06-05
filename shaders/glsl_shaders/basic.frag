#version 330 core

in vec2 TexCoord_FS;
in vec3 Normal_FS;
in vec3 FragPos_FS;
in vec4 Color_FS;

out vec4 FragColor;

void main() {
    FragColor = Color_FS;
}