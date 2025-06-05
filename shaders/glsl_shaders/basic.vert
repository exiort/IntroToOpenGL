#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;  
layout (location = 3) in vec4 aColor;   

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 TexCoord_FS;
out vec3 Normal_FS; 
out vec3 FragPos_FS; 
out vec4 Color_FS;   

void main() {
    FragPos_FS = vec3(model * vec4(aPos, 1.0));
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord_FS = aTexCoord;
    Normal_FS = mat3(transpose(inverse(model))) * aNormal; 
    Color_FS = aColor;
}