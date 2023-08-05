//
// Created by vigi99 on 25/09/20.
//

#pragma once

#include <unordered_map>
#include <utility>
#include <sys/stat.h>
#include "iostream"
#include "Defines.h"

class Helpers {
public:
    static int NullDistanceResults(const xstring &string1, const xstring &string2, double maxDistance) {
        if (string1.empty())
            return (string2.empty()) ? 0 : (string2.size() <= maxDistance) ? string2.size() : -1;
        return (string1.size() <= maxDistance) ? string1.size() : -1;
    }

    static int NullSimilarityResults(const xstring &string1, const xstring &string2, double minSimilarity) {
        return (string1.empty() && string2.empty()) ? 1 : (0 <= minSimilarity) ? 0 : -1;
    }

    static void PrefixSuffixPrep(xstring string1, xstring string2, int &len1, int &len2, int &start) {
        len2 = string2.size();
        len1 = string1.size(); // this is also the minimum length of the two strings
        // suffix common to both strings can be ignored
        while (len1 != 0 && string1[len1 - 1] == string2[len2 - 1]) {
            len1 = len1 - 1;
            len2 = len2 - 1;
        }
        // prefix common to both strings can be ignored
        start = 0;
        while (start != len1 && string1[start] == string2[start]) start++;
        if (start != 0) {
            len2 -= start; // length of the part excluding common prefix and suffix
            len1 -= start;
        }
    }

    static double ToSimilarity(int distance, int length) {
        return (distance < 0) ? -1 : 1 - (distance / (double) length);
    }

    static int ToDistance(double similarity, int length) {
        return (int) ((length * (1 - similarity)) + .0000000001);
    }

    static int CompareTo(int64_t mainValue, int64_t compareValue) {
        if (mainValue == compareValue)
            return 0;
        else if (mainValue > compareValue)
            return 1;
        else
            return -1;
    }

    static bool file_exists (const std::string& name) {
        struct stat buffer;
        return (stat (name.c_str(), &buffer) == 0);
    }
};

template<class T>
class ChunkArray {
private:
    const int ChunkSize = 4096; //this must be a power of 2, otherwise can't optimize Row and Col functions
    const int DivShift = 12; // number of bits to shift right to do division by ChunkSize (the bit position of ChunkSize)
    int Row(unsigned int index) { return index >> DivShift; } // same as index / ChunkSize
    int Col(unsigned int index) { return index & (ChunkSize - 1); } //same as index % ChunkSize
    int Capacity() { return Values.size() * ChunkSize; }

public:
    std::vector<std::vector<T>> Values;
    int Count;

    ChunkArray() {
        Count = 0;
    }

    void Reserve(int initialCapacity) {
        int chunks = (initialCapacity + ChunkSize - 1) / ChunkSize;
        Values.resize(chunks);
        for (int i = 0; i < chunks; ++i) {
            Values[i].resize(ChunkSize);
        }
    }

    int Add(T &value) {
        if (Count == Capacity()) {
            Values.push_back(std::vector<T>());
            Values[Values.size() - 1].resize(ChunkSize);
        }

        int row = Row(Count);
        int col = Col(Count);

        Values[row][col] = value;
        return Count++;
    }

    void Clear() {
        Count = 0;
    }

    T &At(unsigned int index) {
        return Values[Row(index)][Col(index)];
    }

    void Set(unsigned int index, T &value) {
        Values[Row(index)][Col(index)] = value;
    }
};

class Node {
public:
    xstring suggestion;
    int next;
};

class Entry {
public:
    int count;
    int first;
};

class SuggestionStage {
private:
    std::unordered_map<int, Entry> Deletes;
    ChunkArray<Node> Nodes;

public:
    explicit SuggestionStage(int initialCapacity) {
        Deletes.reserve(initialCapacity);
        Nodes.Reserve(initialCapacity * 2);
    }

    int DeleteCount() { return Deletes.size(); }

    int NodeCount() const { return Nodes.Count; }

    void Clear() {
        Deletes.clear();
        Nodes.Clear();
    }

    void Add(int deleteHash, xstring suggestion) {
        auto deletesFinded = Deletes.find(deleteHash);
        Entry newEntry{};
        newEntry.count = 0;
        newEntry.first = -1;
        Entry entry = (deletesFinded == Deletes.end()) ? newEntry : deletesFinded->second;
        int next = entry.first;
        entry.count++;
        entry.first = Nodes.Count;
        Deletes[deleteHash] = entry;
        Node item;
        item.suggestion = std::move(suggestion);
        item.next = next; // 1st semantic errors, this should not be Nodes.Count
        Nodes.Add(item);
    }

    void CommitTo(std::shared_ptr<std::unordered_map<int, std::vector<xstring>>> permanentDeletes) {
        auto permanentDeletesEnd = permanentDeletes->end();
        for (auto &Delete : Deletes) {
            auto permanentDeletesFinded = permanentDeletes->find(Delete.first);
            std::vector<xstring> suggestions;
            int i;
            if (permanentDeletesFinded != permanentDeletesEnd) {
                suggestions = permanentDeletesFinded->second;
                i = suggestions.size();

                std::vector<xstring> newSuggestions;
                newSuggestions.reserve(suggestions.size() + Delete.second.count);
                std::copy(suggestions.begin(), suggestions.end(), back_inserter(newSuggestions));
            } else {
                i = 0;
                int32_t count = Delete.second.count;
                suggestions.reserve(count);
            }

            int next = Delete.second.first;
            while (next >= 0) {
                auto node = Nodes.At(next);
                suggestions.push_back(node.suggestion);
                next = node.next;
                ++i;
            }
            (*permanentDeletes)[Delete.first] = suggestions;
        }
    }
};


class SuggestItem {
public:
    xstring term;
    int distance = 0;
    int64_t count = 0;

    SuggestItem() = default;


    SuggestItem(xstring term, int distance, int64_t count) {
        this->term = std::move(term);
        this->distance = distance;
        this->count = count;
    }

    int CompareTo(const SuggestItem &other) const {
        int disCom = Helpers::CompareTo(this->distance, other.distance);
        if (disCom != 0)
            return disCom;
        int cntCom = Helpers::CompareTo(other.count, this->count);
        if (cntCom != 0)
            return cntCom;
        return this->term.compare(other.term);
    }

    bool Equals(const SuggestItem &obj) const {
        return this->term == obj.term && this->distance == obj.distance && this->count == obj.count;
    }

    int GetHashCode() const {
        return std::hash<xstring>{}(this->term);
    }

    xstring Tostring() const {
        return XL("{") + term + XL(", ") + to_xstring(distance) + XL(", ") + to_xstring(count) + XL("}");
    }

    static bool compare(const SuggestItem &s1, const SuggestItem &s2) {
        return s1.CompareTo(s2) < 0;
    }

    void set(const SuggestItem &exam) {
        this->term = exam.term;
        this->distance = exam.distance;
        this->count = exam.count;
    }
};