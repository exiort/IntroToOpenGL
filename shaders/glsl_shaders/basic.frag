#version 330 core

in vec2 TexCoord_FS;
in vec3 Normal_FS;
in vec3 FragPos_FS;
in vec4 Color_FS;

out vec4 FragColor;

uniform sampler2D texture1;
uniform sampler2D texture2;
uniform float blendFactor;

uniform bool useRawColor;
uniform vec4 rawColor;

void main() {
    if (useRawColor) {
        FragColor = rawColor;
    }
    else {
    	vec4 color1 = texture(texture1, TexCoord_FS);	 
	vec4 color2 = texture(texture2, TexCoord_FS);
        FragColor = mix(color1, color2, blendFactor);
    }
}