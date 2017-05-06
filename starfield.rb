###
#
# Starfield visualisation
#
# This implementation borrows heavily from Michael Baudino's gosu-starfield project 
# (https://github.com/michaelbaudino/gosu-starfield) which is licensed under the 
# MIT License. These modifications are licensed under the same terms
#
# The original work is Copyright (c) 2015 Michael Baudino
# These modifications are Copyright (c) 2017 Arthur Taylor
#
###

require 'arduino-lights'

class Star
  def initialize(starfield, birth_radius = nil)
    @starfield = starfield
    birth_radius ||= [@starfield.width / 2, @starfield.height / 2].max
    @x = rand(-birth_radius..birth_radius)
    @y = rand(-birth_radius..birth_radius)
    @pixel_x = @starfield.to_pixel_x(@x)
    @pixel_y = @starfield.to_pixel_y(@y)
  end

  def clear
    @starfield.draw_star(@pixel_x, @pixel_y, false)
  end

  def draw
    @starfield.draw_star(@pixel_x, @pixel_y, true)
  end

  def update
    @x *= @starfield.velocity
    @y *= @starfield.velocity
    new_x = @starfield.to_pixel_x(@x)
    new_y = @starfield.to_pixel_y(@y)
    if (new_x != @pixel_x || new_y != @pixel_y)
      @starfield.draw_star(@pixel_x, @pixel_y, false)
    end
    @pixel_x = new_x
    @pixel_y = new_y
  end

  def out_of_viewport?
    @x < -@starfield.width / 2 ||
    @x >  @starfield.width / 2 ||
    @y < -@starfield.height    ||
    @y >  @starfield.height
  end
end

class Starfield
  attr_reader :velocity, :width, :height

  def initialize(width, height)
    @width     = width
    @height    = height
    @max_stars = 10
    @stars     = Array.new(@max_stars) { Star.new(self) }
    @velocity  = 1.02
  end

  def to_pixel_x(x)
    (((x + @width / 2) * 12.0) / @width).to_i
  end

  def to_pixel_y(y)
    (((y + @height / 2) * 12.0) / @height).to_i
  end

  def draw
    @stars.each &:draw
    ArduinoLights::end_frame()
  end

  def update
    kill_old_stars
    create_new_stars
    @stars.each &:update
  end

  def stars_count
    @stars.count
  end

  def draw_star(x, y, visible)
    colour = visible ? 253 : 0
    if (x < 0 || x > 11 || y < 0 || y > 11)
      return
    end
    ArduinoLights::set_pixel_xy(x, y, colour, colour, colour)
  end

private

  def create_new_stars
    missing_stars = [0, @max_stars - stars_count].max
    @stars += Array.new(missing_stars) { Star.new(self, [@width, @height].sample / 10) }
  end

  def kill_old_stars
    @stars.each do |star|
      if star.out_of_viewport?
        star.clear
        @stars.delete(star)
      end
    end
  end

end

starfield = Starfield.new(120,120)
while (true)
  starfield.update
  starfield.draw
end

