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

#define DEBUGI

uint32_t interval_boundaries[4] = {};

int check_overlaps(string_view current_line){
    constexpr std::string_view delim { "," };
    constexpr std::string_view num_delim { "-" };
    uint8_t index = 0;
    for (auto i: current_line | std::views::split(delim)) {
        auto numbers = i | std::views::split(num_delim)
                         | std::ranges::views::transform([](auto&& str) { 
                                    return std::stoi(std::string_view(&*str.begin(),
                                        std::ranges::distance(str)).data(), nullptr, 10); });
        for (auto num : numbers){
            interval_boundaries[index++] = num;
            #ifdef DEBUG
            std::cout << num << " ";
            #endif
        }
    };
    #ifdef DEBUG
    std::cout << "\n";
    #endif
    int full_overlap = 0;
    int partial_overlap = 0;
    if (interval_boundaries[0] >= interval_boundaries[2] && interval_boundaries[1] <= interval_boundaries[3]) {
        full_overlap = 2;
    }
    if (interval_boundaries[0] <= interval_boundaries[2] && interval_boundaries[1] >= interval_boundaries[3]) {
        full_overlap = 2;
    }
    if ( (interval_boundaries[0] <= interval_boundaries[2] && interval_boundaries[2] <= interval_boundaries[1]) ||
         (interval_boundaries[0] <= interval_boundaries[3] && interval_boundaries[3] <= interval_boundaries[1]) ||
         (interval_boundaries[2] <= interval_boundaries[0] && interval_boundaries[0] <= interval_boundaries[3]) ||
         (interval_boundaries[2] <= interval_boundaries[1] && interval_boundaries[1] <= interval_boundaries[3]) )
    {
        #ifdef DEBUG
        std::cout << interval_boundaries[0] << " <= " << interval_boundaries[2] << " <= " << interval_boundaries[1] << '\n';
        std::cout << interval_boundaries[0] << " <= " << interval_boundaries[3] << " <= " << interval_boundaries[1] << '\n';
        std::cout << interval_boundaries[2] << " <= " << interval_boundaries[0] << " <= " << interval_boundaries[3] << '\n';
        std::cout << interval_boundaries[2] << " <= " << interval_boundaries[1] << " <= " << interval_boundaries[3] << '\n';
        #endif
        partial_overlap = 1;
    }
    return full_overlap | partial_overlap;
}

int main() {
    std::ifstream is("day4.input");
    //std::ifstream is("day4.small");
    std::stringstream buffer;
    buffer << is.rdbuf();
    is.close();
    std::string input_data = buffer.str();
    auto lines = input_data 
        | std::ranges::views::split('\n')
        | std::ranges::views::transform([](auto &&rng) {
            return std::string_view(&*rng.begin(), ranges::distance(rng));});

    int counter = 0;
    int partial_overlaps = 0;
    string group = "";
    int line_counter = 0;
    int overlaps_results = 0;
    for (auto&& line : lines)
    {   
        overlaps_results = check_overlaps(line);
        partial_overlaps += 1 & overlaps_results;
        counter += 1 & overlaps_results >> 1;
        #ifdef DEBUG
        std::cout << "check_overlaps output: " << check_overlaps(line) << '\n';
        std::cout << line_counter++ << '\t' << (1 & check_overlaps(line)) << "\n";
        #endif
    }
    std::cout << counter << '\n';
    std::cout << partial_overlaps << '\n';
    return 0;
}
