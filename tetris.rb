require 'arduino-lights'

@colors = [
  [ 253, 0, 0 ],
  [ 253, 253, 0 ],
  [ 0, 253, 0 ],
  [ 0, 253, 253 ],
  [ 0, 0, 253 ]
]

@shapes = [
  [ [ 1, 1, 1, 1 ], 
    [ 0, 0, 0, 0 ] ],

  [ [ 1, 1, 0 ], 
    [ 0, 1, 1 ] ],

  [ [ 1, 1, 1 ], 
    [ 0, 1, 0 ] ],

  [ [ 1, 1, 1 ],
    [ 0, 0, 1 ] ],

  [ [ 1, 1 ],
    [ 1, 1 ] ]
]

class Block

  def initialize(shape, rotation, color, startx)
    @shape = Block::transform(shape, rotation) 
    @x = [ startx, 11 - @shape[0].size ].min
    @y = 1 - @shape.size 
    @color = color
  end

  def fall
    @y = @y + 1
  end

  def off_screen?
    @y > 11
  end

  def draw(black = false)
    color = black ? [0,0,0] : @color
    @shape.each_with_index do |row, sy|
      row.each_with_index do |pixel, sx|
        if pixel == 1
          if @x + sx < 12 and @y + sy < 12 and @y + sy >= 0
            ArduinoLights::set_pixel_xy(@x + sx, @y + sy,
                                         color[0], color[1], color[2])
          end
        end
      end
    end
  end

  def clear
    self.draw(true)
  end

  class << self

    def transform(input_shape, rotation)
      shape = input_shape.clone
      if (rotation % 2 == 1)
        shape = shape.transpose
      end
      if (rotation >= 2)
        shape = shape.collect { |row| row.reverse }
      end
      shape
    end

  end

end

def clear_screen
  (0..11).each do |x|
    (0..11).each do |y|
      ArduinoLights::set_pixel_xy(x, y, 0, 0, 0)
    end
  end
end

clear_screen
blocks = []
frame = 0
while true do
  if frame % 4 == 0
    blocks << Block.new(@shapes.sample, rand(4), @colors.sample, rand(12))
  end
  blocks.each do |block|
    block.clear
    block.fall
    block.draw
  end
  blocks.delete_if(&:off_screen?)
  ArduinoLights::end_frame()
  frame = frame + 1
  sleep(0.5)
end
