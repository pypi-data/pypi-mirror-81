/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtCore module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

/* This file is autogenerated from the Unicode 10.0 database. Do not edit */

//
//  W A R N I N G
//  -------------
//
// This file is not part of the Qt API.  It exists for the convenience
// of internal files.  This header file may change from version to version
// without notice, or even be removed.
//
// We mean it.
//

#ifndef QUNICODETABLES_P_H
#define QUNICODETABLES_P_H

#include <QtCore/private/qglobal_p.h>

#include <QtCore/qchar.h>

QT_BEGIN_NAMESPACE

#define UNICODE_DATA_VERSION QChar::Unicode_10_0

namespace QUnicodeTables {

struct Properties {
    ushort category            : 8; /* 5 used */
    ushort direction           : 8; /* 5 used */
    ushort combiningClass      : 8;
    ushort joining             : 3;
    signed short digitValue    : 5;
    signed short mirrorDiff    : 16;
    ushort lowerCaseSpecial    : 1;
    signed short lowerCaseDiff : 15;
#ifdef Q_OS_WASM
    unsigned char              : 0; //wasm 64 packing trick
#endif
    ushort upperCaseSpecial    : 1;
    signed short upperCaseDiff : 15;
    ushort titleCaseSpecial    : 1;
    signed short titleCaseDiff : 15;
    ushort caseFoldSpecial     : 1;
    signed short caseFoldDiff  : 15;
    ushort unicodeVersion      : 8; /* 5 used */
    ushort nfQuickCheck        : 8;
#ifdef Q_OS_WASM
    unsigned char              : 0; //wasm 64 packing trick
#endif
    ushort graphemeBreakClass  : 5; /* 5 used */
    ushort wordBreakClass      : 5; /* 5 used */
    ushort sentenceBreakClass  : 8; /* 4 used */
    ushort lineBreakClass      : 6; /* 6 used */
    ushort script              : 8;
};

Q_CORE_EXPORT const Properties * QT_FASTCALL properties(uint ucs4) Q_DECL_NOTHROW;
Q_CORE_EXPORT const Properties * QT_FASTCALL properties(ushort ucs2) Q_DECL_NOTHROW;

struct LowercaseTraits
{
    static inline signed short caseDiff(const Properties *prop)
    { return prop->lowerCaseDiff; }
    static inline bool caseSpecial(const Properties *prop)
    { return prop->lowerCaseSpecial; }
};

struct UppercaseTraits
{
    static inline signed short caseDiff(const Properties *prop)
    { return prop->upperCaseDiff; }
    static inline bool caseSpecial(const Properties *prop)
    { return prop->upperCaseSpecial; }
};

struct TitlecaseTraits
{
    static inline signed short caseDiff(const Properties *prop)
    { return prop->titleCaseDiff; }
    static inline bool caseSpecial(const Properties *prop)
    { return prop->titleCaseSpecial; }
};

struct CasefoldTraits
{
    static inline signed short caseDiff(const Properties *prop)
    { return prop->caseFoldDiff; }
    static inline bool caseSpecial(const Properties *prop)
    { return prop->caseFoldSpecial; }
};

enum GraphemeBreakClass {
    GraphemeBreak_Any,
    GraphemeBreak_CR,
    GraphemeBreak_LF,
    GraphemeBreak_Control,
    GraphemeBreak_Extend,
    GraphemeBreak_ZWJ,
    GraphemeBreak_RegionalIndicator,
    GraphemeBreak_Prepend,
    GraphemeBreak_SpacingMark,
    GraphemeBreak_L,
    GraphemeBreak_V,
    GraphemeBreak_T,
    GraphemeBreak_LV,
    GraphemeBreak_LVT,
    Graphemebreak_E_Base,
    Graphemebreak_E_Modifier,
    Graphemebreak_Glue_After_Zwj,
    Graphemebreak_E_Base_GAZ,
    NumGraphemeBreakClasses,
};

enum WordBreakClass {
    WordBreak_Any,
    WordBreak_CR,
    WordBreak_LF,
    WordBreak_Newline,
    WordBreak_Extend,
    WordBreak_ZWJ,
    WordBreak_Format,
    WordBreak_RegionalIndicator,
    WordBreak_Katakana,
    WordBreak_HebrewLetter,
    WordBreak_ALetter,
    WordBreak_SingleQuote,
    WordBreak_DoubleQuote,
    WordBreak_MidNumLet,
    WordBreak_MidLetter,
    WordBreak_MidNum,
    WordBreak_Numeric,
    WordBreak_ExtendNumLet,
    WordBreak_E_Base,
    WordBreak_E_Modifier,
    WordBreak_Glue_After_Zwj,
    WordBreak_E_Base_GAZ,
    NumWordBreakClasses,
};

enum SentenceBreakClass {
    SentenceBreak_Any,
    SentenceBreak_CR,
    SentenceBreak_LF,
    SentenceBreak_Sep,
    SentenceBreak_Extend,
    SentenceBreak_Sp,
    SentenceBreak_Lower,
    SentenceBreak_Upper,
    SentenceBreak_OLetter,
    SentenceBreak_Numeric,
    SentenceBreak_ATerm,
    SentenceBreak_SContinue,
    SentenceBreak_STerm,
    SentenceBreak_Close,
    NumSentenceBreakClasses
};

// see http://www.unicode.org/reports/tr14/tr14-30.html
// we don't use the XX and AI classes and map them to AL instead.
enum LineBreakClass {
    LineBreak_OP, LineBreak_CL, LineBreak_CP, LineBreak_QU, LineBreak_GL,
    LineBreak_NS, LineBreak_EX, LineBreak_SY, LineBreak_IS, LineBreak_PR,
    LineBreak_PO, LineBreak_NU, LineBreak_AL, LineBreak_HL, LineBreak_ID,
    LineBreak_IN, LineBreak_HY, LineBreak_BA, LineBreak_BB, LineBreak_B2,
    LineBreak_ZW, LineBreak_CM, LineBreak_WJ, LineBreak_H2, LineBreak_H3,
    LineBreak_JL, LineBreak_JV, LineBreak_JT, LineBreak_RI, LineBreak_CB,
    LineBreak_EB, LineBreak_EM, LineBreak_ZWJ,
    LineBreak_SA, LineBreak_SG, LineBreak_SP,
    LineBreak_CR, LineBreak_LF, LineBreak_BK,
    NumLineBreakClasses
};

Q_CORE_EXPORT GraphemeBreakClass QT_FASTCALL graphemeBreakClass(uint ucs4) Q_DECL_NOTHROW;
inline GraphemeBreakClass graphemeBreakClass(QChar ch) Q_DECL_NOTHROW
{ return graphemeBreakClass(ch.unicode()); }

Q_CORE_EXPORT WordBreakClass QT_FASTCALL wordBreakClass(uint ucs4) Q_DECL_NOTHROW;
inline WordBreakClass wordBreakClass(QChar ch) Q_DECL_NOTHROW
{ return wordBreakClass(ch.unicode()); }

Q_CORE_EXPORT SentenceBreakClass QT_FASTCALL sentenceBreakClass(uint ucs4) Q_DECL_NOTHROW;
inline SentenceBreakClass sentenceBreakClass(QChar ch) Q_DECL_NOTHROW
{ return sentenceBreakClass(ch.unicode()); }

Q_CORE_EXPORT LineBreakClass QT_FASTCALL lineBreakClass(uint ucs4) Q_DECL_NOTHROW;
inline LineBreakClass lineBreakClass(QChar ch) Q_DECL_NOTHROW
{ return lineBreakClass(ch.unicode()); }

} // namespace QUnicodeTables

QT_END_NAMESPACE

#endif // QUNICODETABLES_P_H
