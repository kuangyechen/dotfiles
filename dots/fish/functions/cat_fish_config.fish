function cat_fish_config --wraps='cat {$HOME}/.config/fish/config.fish' --wraps='cat ~/.config/fish/config.fish' --description 'alias cat_fish_config cat ~/.config/fish/config.fish'
  cat ~/.config/fish/config.fish $argv
        
end
