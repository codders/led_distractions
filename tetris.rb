require 'arduino-lights'

@colors = [
  [ 253, 0, 0 ],
  [ 253, 253, 0 ],
  [ 0, 253, 0 ],
  [ 0, 253, 253 ],
  [ 0, 0, 253 ]
]

@shapes = [
  [ [ 1, 1, 1, 1 ] ],

  [ [ 1, 1, 0 ], 
    [ 0, 1, 1 ] ],

  [ [ 1, 1, 1 ], 
    [ 0, 1, 0 ] ],

  [ [ 1, 1, 1 ],
    [ 0, 0, 1 ] ],

  [ [ 1, 1 ],
    [ 1, 1 ] ]
]

class Screen

  def initialize
    reset
  end

  def reset
    @buffer = (0..11).collect { |c| (0..11).collect { |c| [0,0,0] } }
  end

  def set_pixel_xy(x, y, r, g, b)
    @buffer[y][x] = [r, g, b] 
  end

  def draw
    @buffer.each_with_index do |row, y|
      row.each_with_index do |pixel, x|
        ArduinoLights::set_pixel_xy(x, y, pixel[0], pixel[1], pixel[2])
      end
    end
    ArduinoLights::end_frame()
  end

  def collision(block, x, y)
    block.shape.each_with_index do |row, sy|
      next if sy + y < 0 or sy + y > 11
      row.each_with_index do |pixel, sx|
        if block.shape[sy][sx] != 0 and @buffer[y + sy][x + sx] != [0, 0, 0] and !block.contains?(x + sx, y + sy)
          return true
        end
      end
    end
    false
  end

end

class Block

  attr_reader :shape

  def initialize(shape, rotation, color, startx)
    @shape = Block::transform(shape, rotation) 
    @x = [ startx, 11 - @shape[0].size ].min
    @y = 1 - @shape.size 
    @color = color
  end

  def can_fall?(screen)
    if @y + @shape.size >= 12
      return false
    end
    return !screen.collision(self, @x, @y + 1)
  end

  def fall(screen)
    if can_fall?(screen)
      @y = @y + 1
    end
  end

  def off_screen?
    @y > 11
  end

  def contains?(x, y)
    return (x - @x >= 0) && (y - @y >= 0) && (x - @x < @shape[0].size) && (y - @y < @shape.size) && (@shape[y - @y][x - @x] == 1)
  end

  def in_collision?(screen)
    screen.collision(self, @x, @y)
  end

  def draw(screen, black = false)
    color = black ? [0,0,0] : @color
    @shape.each_with_index do |row, sy|
      row.each_with_index do |pixel, sx|
        if pixel == 1
          if @x + sx < 12 and @y + sy < 12 and @y + sy >= 0
            screen.set_pixel_xy(@x + sx, @y + sy,
                                color[0], color[1], color[2])
          end
        end
      end
    end
  end

  def clear(screen)
    self.draw(screen, true)
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

screen = Screen.new
screen.draw

blocks = []

frame = 0
while true do
  if frame % 4 == 0
    new_block = Block.new(@shapes.sample, rand(4), @colors.sample, rand(12))
    if new_block.can_fall?(screen)
      blocks << new_block
    else
      puts "Screen is full. Resetting"
      blocks = []
      screen = Screen.new
      screen.draw
    end
  end
  blocks.each do |block|
    if block.can_fall?(screen)
      block.clear(screen)
      block.fall(screen)
      block.draw(screen) unless block.in_collision?(screen)
    end
  end
  screen.draw
  frame = frame + 1
  sleep(0.5)
end
