function cat_fish_variables --wraps='cat {$HOME}/.config/fish/fish_variables' --wraps='cat ~/.config/fish/fish_variables' --description 'alias cat_fish_variables cat ~/.config/fish/fish_variables'
  cat ~/.config/fish/fish_variables $argv
        
end
