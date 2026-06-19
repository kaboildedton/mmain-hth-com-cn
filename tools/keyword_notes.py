from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class KeywordNote:
    keyword: str
    note: str
    url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "note": self.note,
            "url": self.url,
            "tags": self.tags,
            "created_at": self.created_at
        }

    def formatted_output(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return (
            f"关键词: {self.keyword}\n"
            f"备注: {self.note}\n"
            f"URL: {self.url}\n"
            f"标签: {tag_str}\n"
            f"创建时间: {self.created_at}\n"
        )

@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)
    name: str = "默认集合"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_by_keyword(self, keyword: str) -> bool:
        for i, n in enumerate(self.notes):
            if n.keyword == keyword:
                del self.notes[i]
                return True
        return False

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def list_all(self, separator: str = "-" * 40) -> str:
        if not self.notes:
            return "当前集合为空。"
        parts = [f"集合名称: {self.name}", f"笔记数量: {len(self.notes)}"]
        for idx, note in enumerate(self.notes, 1):
            parts.append(f"条目 {idx}:")
            parts.append(note.formatted_output())
            parts.append(separator)
        return "\n".join(parts)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            [note.to_dict() for note in self.notes],
            ensure_ascii=False,
            indent=indent
        )

    def export_markdown(self) -> str:
        lines = [f"# {self.name}\n"]
        for note in self.notes:
            lines.append(f"## {note.keyword}")
            lines.append(f"- **备注**: {note.note}")
            lines.append(f"- **URL**: {note.url}")
            tag_str = ", ".join(f"`{t}`" for t in note.tags) if note.tags else "无"
            lines.append(f"- **标签**: {tag_str}")
            lines.append(f"- **创建时间**: {note.created_at}")
            lines.append("")
        return "\n".join(lines)

def create_sample_notes() -> NoteCollection:
    collection = NoteCollection(name="华体会相关笔记")
    note1 = KeywordNote(
        keyword="华体会",
        note="华体会是一个综合性体育娱乐平台，提供多种体育赛事和游戏体验。",
        url="https://mmain-hth.com.cn",
        tags=["体育", "娱乐", "平台"]
    )
    note2 = KeywordNote(
        keyword="华体会注册",
        note="用户可通过官网或移动端注册华体会账号，流程简便快捷。",
        url="https://mmain-hth.com.cn/register",
        tags=["注册", "指南"]
    )
    note3 = KeywordNote(
        keyword="华体会活动",
        note="平台定期推出优惠活动和赛事竞猜，吸引用户参与互动。",
        url="https://mmain-hth.com.cn/promotions",
        tags=["活动", "优惠"]
    )
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    return collection

def main():
    collection = create_sample_notes()
    print("=== 列出所有笔记 ===")
    print(collection.list_all())
    print("\n=== 按标签查找 ===")
    tag_notes = collection.find_by_tag("体育")
    for note in tag_notes:
        print(note.formatted_output())
    print("\n=== 导出 JSON ===")
    print(collection.to_json())
    print("\n=== 导出 Markdown ===")
    print(collection.export_markdown())

if __name__ == "__main__":
    main()