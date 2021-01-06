uniform sampler2D bgl_RenderedTexture;

uniform float offset_amount = 2.5;
uniform float threshold = 0.75;
uniform int blur_sample = 2;
uniform float blur_size = 0.002;
int x=0;
int y=0;


vec4 brightness(vec4 current_color){
    current_color = max(current_color-threshold, 0.0);
    return current_color;
}
void main()
{
    vec4 new_color = vec4(0);
    for (x=-blur_sample; x <= blur_sample; x++){
        for (y=-blur_sample; y<= blur_sample; y++){
            vec2 offset = vec2(x,y) * blur_size;
            new_color += brightness(texture2D(bgl_RenderedTexture, gl_TexCoord[0].st + offset, offset_amount));
        }
        
    }
    new_color /= ((blur_sample*2)+1)*((blur_sample*2)+1);
    gl_FragColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st, 0.0)+new_color;
}