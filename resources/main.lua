-- main.lua
function love.load()
    love.window.setTitle("My Love2D Game")
    love.graphics.setBackgroundColor(0.1, 0.1, 0.1)
end

function love.update(dt)
    -- Game logic goes here
end

function love.draw()
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Hello, Love2D!", 400, 300)
end