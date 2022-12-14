#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <ranges>
#include <iomanip>
#include <string_view>
#include <charconv>
#include <map>
#include <vector>
#include <iomanip>
#include <algorithm>
#include <charconv>

using namespace std;

int main() {
    std::ifstream is("day1.input");
    std::stringstream buffer;
    buffer << is.rdbuf();
    is.close();
    std::string input_data = buffer.str();
    auto lines = input_data 
        | std::ranges::views::split('\n')
        | std::ranges::views::transform([](auto&& str) { 
            return std::stoi(std::string_view(&*str.begin(),
                                    std::ranges::distance(str)).data(), nullptr, 10); });
    int prev_line = -1;
    int elfs = 0;
    int max_elf = 0;
    int current_elf = 0;
    std::vector<int> elf_callories;
    for (auto&& line : lines)
    {   
        if (line == prev_line) {
            elfs++;
            current_elf -= prev_line;
            if (current_elf > max_elf) {
                max_elf = current_elf;
            }
            elf_callories.push_back(current_elf);
            current_elf = 0;
        }
        #ifdef DEBUG
        std::cout << line << "\n";
        #endif
        prev_line = line;
        current_elf += line;
    }
    std::cout << max_elf << "\n";
    sort(elf_callories.begin(), elf_callories.end());
    int top_n_elfs_sum = 0;
    for (size_t top_n_elfs=0; top_n_elfs < 3; top_n_elfs++){
        #ifdef DEBUG
        std::cout << elf_callories[elf_callories.size()-1-top_n_elfs] << "\n";
        #endif
        top_n_elfs_sum += elf_callories[elf_callories.size()-1-top_n_elfs];
    }
    std::cout << top_n_elfs_sum << "\n";
    return 0;
}
