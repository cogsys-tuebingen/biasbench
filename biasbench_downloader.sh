#!/bin/bash

# Allowed datasets
ALLOWED_DATASETS=("led" "led/data_set" "led/validation_set_files" "robot_arm" "robot_arm/left_right" "robot_arm/triangle" "spinning_dot" "spinning_dot/black_dot" "spinning_dot/grey_dot")
# Allowed sizes
ALLOWED_SIZES=("small" "medium" "large" "full")

# Predefined wget commands for sizes
WGET_CMDS=(
    ".*/(-20|-1?[0-9]|[0-7]?[0-9]|80)_([3-9][0-9]|1[0-2][0-9]|130)_.*)' https://www.cogsys.cs.uni-tuebingen.de/webprojects/biasbench-2025/files/"
    "*/(-20|-1?[0-9]|[0-9]?[0-9]|1[0-2][0-9]|130)_([3-9][0-9]|1[0-7][0-9]|180)_.*)' https://www.cogsys.cs.uni-tuebingen.de/webprojects/biasbench-2025/files/"
    ".*/(-70|-[1-6]?[0-9]|[0-9]?[0-9]|1[0-2][0-9]|130)_(-20|-1?[0-9]|[0-9]?[0-9]|1[0-7][0-9]|180)_.*)' https://www.cogsys.cs.uni-tuebingen.de/webprojects/biasbench-2025/files/"
    ".*) https://www.cogsys.cs.uni-tuebingen.de/webprojects/biasbench-2025/files/"
)

print_usage() {
    echo "Usage:"
    echo "  $0 <size>"
    echo "    where <size> is one of: small, medium, large, full"
    echo "  $0 <dataset1,dataset2,...> <range1> [<range2> ... <range5>]"
    echo "    where datasets are from: ${ALLOWED_DATASETS[*]}"
    echo "    and ranges are like 0-5, 2-, -4 (open-ended allowed)"
}

# Check if value is in array
in_array() {
    local val="$1"; shift
    for item; do [[ "$item" == "$val" ]] && return 0; done
    return 1
}



# reggex_size2: builds regex for two-digit numbers
reggex_size2() {
    local min=$1
    local max=$2
    local leading_zeroes=$3
    if (( max < 10 )); then
        if [[ "$leading_zeroes" == "true" ]]; then
            echo "(0[$min-$max])"
        else
            echo "[$min-$max]"
        fi
        return
    fi
    if (( max / 10 == min / 10 )); then
        echo "($((max / 10))[$((min % 10))-$((max % 10))])"
        return
    fi
    if (( max / 10 == min / 10 + 1 )); then
        if (( min < 10 )) && [[ "$leading_zeroes" != "true" ]]; then
            echo "($((max / 10))[0-$((max % 10))]|[$((min % 10))-9])"
        else
            echo "($((max / 10))[0-$((max % 10))]|$((min / 10))[$((min % 10))-9])"
        fi
        return
    fi
    if (( min < 10 )) && [[ "$leading_zeroes" != "true" ]]; then
        echo "($((max / 10))[0-$((max % 10))]|[$((min % 10))-9]|[$((min / 10 + 1))-$((max / 10 - 1))][0-9])"
    else
        echo "($((max / 10))[0-$((max % 10))]|$((min / 10))[$((min % 10))-9]|[$((min / 10 + 1))-$((max / 10 - 1))][0-9])"
    fi
}

# reggex_range: builds regex for a range
reggex_range() {
    local min=$1
    local max=$2
    if (( min == max )); then
        echo "$min"
        return
    fi
    if (( min == 0 && max >= 199 )); then
        echo "[0-9]+"
        return
    fi
    if (( max < 10 )); then
        echo "[$min-$max]"
        return
    fi
    if (( max < 100 )); then
        reggex_size2 "$min" "$max"
        return
    fi
    if (( min >= 100 )); then
        echo "(1$(reggex_size2 $((min-100)) $((max-100)) true))"
        return
    fi
    echo "($(reggex_size2 $min 99)|1$(reggex_size2 0 $((max-100)) true))"
}

# give_reggex_range: main function

# Usage: give_reggex_range <range_string>
give_reggex_range() {
    local rangestring="$1"
    IFS=':' read -r min max <<< "$rangestring"
    [[ -z "$min" ]] && min=-199
    [[ -z "$max" ]] && max=199
    min=$(( min < -199 ? -199 : (min > 199 ? 199 : min) ))
    max=$(( max < -199 ? -199 : (max > 199 ? 199 : max) ))
    if((min==-199 && max==199)); then
        echo "[+-]?[0-9]+"
        return
    fi
    if (( min >= 0 )); then
        reggex_range "$min" "$max"
        return
    fi
    if (( max == 0 )); then
        echo "(-($(reggex_range $((-max)) $((-min))))|0)"
        return
    fi
    if (( max < 0 )); then
        echo "-$(reggex_range $((-max)) $((-min)))"
        return
    fi
    echo "(-($(reggex_range 0 $((-min))))|$(reggex_range 0 $max))"
}


# Main
if [[ $# -ge 1 ]]; then
    first_arg="$1"
    if in_array "$first_arg" "${ALLOWED_SIZES[@]}"; then
        # SIZE MODE
        size="$1"
        shift
        # If datasets are provided, validate them
        if [[ $# -ge 1 ]]; then
            IFS=',' read -ra DATASETS <<< "$1"
            for ds in "${DATASETS[@]}"; do
                if ! in_array "$ds" "${ALLOWED_DATASETS[@]}"; then
                    echo "Invalid dataset: $ds"
                    print_usage
                    exit 1
                fi
            done
        fi
        # Find index of size
        for idx in "${!ALLOWED_SIZES[@]}"; do
            if [[ "${ALLOWED_SIZES[$idx]}" == "$size" ]]; then
                size_idx=$idx
                break
            fi
        done
        cmd="wget -r -c -np -nH --reject index.html* --accept-regex= '(.*/$| ${WGET_CMDS[$size_idx]}"
        echo "Running wget command for size: $size"
        # Append datasets if provided
        if [[ ${#DATASETS[@]} -gt 0 ]]; then
            for ds in "${DATASETS[@]}"; do
                echo "$cmd$ds/"
            done

        else
            echo "$cmd"
            eval "$cmd"
        fi
        exit 0
    else
        # DATASET MODE
        if [[ "$first_arg" == "all" ]]; then
            DATASETS=("led" "spinning_dot" "robot_arm")
        else
            IFS=',' read -ra DATASETS <<< "$first_arg"
        fi
        shift
        # Validate datasets
        for ds in "${DATASETS[@]}"; do
            if ! in_array "$ds" "${ALLOWED_DATASETS[@]}"; then
                echo "Invalid dataset: $ds"
                print_usage
                exit 1
            fi
        done
        # Parse up to 5 ranges (min:max)
        RANGES=()
        for i in {1..5}; do
            if [[ $# -ge $i ]]; then
                RANGES+=("${!i}")
            else
                RANGES+=(":")
            fi
        done
        # Build regex for ranges using give_reggex_range
        REGEXES=()
        for r in "${RANGES[@]}"; do
            regex_part=$(give_reggex_range "$r")
            REGEXES+=("$regex_part")
        done
        # Join regexes with _
        regex_ranges=$(IFS=_; echo "${REGEXES[*]}")
        # Compose final regex: .*$rangesregex\.h5
        final_regex=".*${regex_ranges}\\.h5"

        # For each dataset, echo a wget command with the dataset appended to the URL
        base_url="https://www.cogsys.cs.uni-tuebingen.de/webprojects/biasbench-2025/files"
        echo "Running wget command:"
        if [[ ${#DATASETS[@]} -gt 0 ]]; then
            for ds in "${DATASETS[@]}"; do
                echo "wget -r -c -np -nH --reject index.html* --accept-regex '(.*/$|$final_regex)' $base_url/$ds/"
                eval "wget -r -c -np -nH --reject index.html* --accept-regex '(.*/$|$final_regex)' $base_url/$ds/"
            done
        else
            echo "wget -r -c -np -nH --reject index.html* --accept-regex '(.*/$|$final_regex)' $base_url/"
            eval "wget -r -c -np -nH --reject index.html* --accept-regex '(.*/$|$final_regex)' $base_url/"
        fi
        exit 0
    fi
else
    echo "Invalid input."
    print_usage
    exit 1
fi
